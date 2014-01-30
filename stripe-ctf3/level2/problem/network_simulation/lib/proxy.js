// This file is a port of [node-http-proxy](https://github.com/nodejitsu/node-http-proxy)
// The purpose of the port is to enable connections to the backend
// server over a Unix socket file.

// node-http-proxy includes the following message:

// Copyright (c) 2010 Charlie Robbins, Mikeal Rogers, Fedor Indutny, & Marak Squires
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:

// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"use strict";

var http = require('http');
var url = require('url')
var events = require('events');
var util = require('util');

var HttpProxy = exports.HttpProxy = function(options) {
  events.EventEmitter.call(this);
  var self  = this;
  this.target = options.target;
  this.enable  = {};
  this.timeout = options.timeout;
}

util.inherits(HttpProxy, events.EventEmitter);

exports.createServer = function (options, callback) {
  var handlers = [callback];
  var proxy = new HttpProxy(options);
  function handler(req, res) {
    return callback(req, res, proxy);
  }
  var server = http.createServer(handler);
  server.on('close', function () {
    proxy.close();
  });
  server.proxy = proxy;
  return server;
}

//
// ### function proxyRequest (req, res, buffer)
// #### @req {ServerRequest} Incoming HTTP Request to proxy.
// #### @res {ServerResponse} Outgoing HTTP Request to write proxied data to.
// #### @buffer {Object} Result from `httpProxy.buffer(req)`
//
HttpProxy.prototype.proxyRequest = function (req, res, buffer) {
  var self = this,
      errState = false,
      outgoing = {},
      reverseProxy,
      location;

  // If this is a DELETE request then set the "content-length"
  // header (if it is not already set)
  if (req.method === 'DELETE') {
    req.headers['content-length'] = req.headers['content-length'] || '0';
  }

  //
  // Add common proxy headers to the request so that they can
  // be availible to the proxy target server. If the proxy is
  // part of proxy chain it will append the address:
  //
  // * `x-forwarded-for`: IP Address of the original request
  // * `x-forwarded-proto`: Protocol of the original request
  // * `x-forwarded-port`: Port of the original request.
  //
  if (this.enable.xforward && req.connection && req.socket) {
    if (req.headers['x-forwarded-for']) {
      var addressToAppend = "," + req.connection.remoteAddress || req.socket.remoteAddress;
      req.headers['x-forwarded-for'] += addressToAppend;
    }
    else {
      req.headers['x-forwarded-for'] = req.connection.remoteAddress || req.socket.remoteAddress;
    }

    if (req.headers['x-forwarded-port']) {
      var portToAppend = "," + getPortFromHostHeader(req);
      req.headers['x-forwarded-port'] += portToAppend;
    }
    else {
      req.headers['x-forwarded-port'] = getPortFromHostHeader(req);
    }

    if (req.headers['x-forwarded-proto']) {
      var protoToAppend = "," + getProto(req);
      req.headers['x-forwarded-proto'] += protoToAppend;
    }
    else {
      req.headers['x-forwarded-proto'] = getProto(req);
    }
  }

  if (this.timeout) {
    req.socket.setTimeout(this.timeout);
  }

  //
  // Emit the `start` event indicating that we have begun the proxy operation.
  //
  this.emit('start', req, res, this.target);

  //
  // #### function proxyError (err)
  // #### @err {Error} Error contacting the proxy target
  // Short-circuits `res` in the event of any error when
  // contacting the proxy target at `host` / `port`.
  //
  function proxyError(err) {
    errState = true;

    //
    // Emit an `error` event, allowing the application to use custom
    // error handling. The error handler should end the response.
    //
    if (self.emit('proxyError', err, req, res)) {
      return;
    }

    res.writeHead(500, { 'Content-Type': 'application/json' });

    if (req.method !== 'HEAD') {
      var contents = {
        'error': err
      }
      res.write(JSON.stringify(contents));
    }

    try { res.end() }
    catch (ex) { console.error("res.end error: %s", ex.message) }
  }

  //
  // Setup outgoing proxy with relevant properties.
  //
  outgoing.host       = this.target.host;
  outgoing.hostname   = this.target.hostname;
  outgoing.port       = this.target.port;
  outgoing.socketPath = this.target.socketPath;
  outgoing.agent      = this.target.agent;
  outgoing.method     = req.method;
  outgoing.path       = url.parse(req.url).path;
  outgoing.headers    = req.headers;

  //
  // If the changeOrigin option is specified, change the
  // origin of the host header to the target URL! Please
  // don't revert this without documenting it!
  //
  if (this.changeOrigin) {
    outgoing.headers.host = this.target.host;
    // Only add port information to the header if not default port
    // for this protocol.
    // See https://github.com/nodejitsu/node-http-proxy/issues/458
    if (this.target.port !== 443 && this.target.https ||
      this.target.port !== 80 && !this.target.https) {
      outgoing.headers.host += ':' + this.target.port;
    }
  }

  //
  // Open new HTTP request to internal resource with will act
  // as a reverse proxy pass
  //
  reverseProxy = http.request(outgoing, function (response) {
    //
    // Process the `reverseProxy` `response` when it's received.
    //
    if (req.httpVersion === '1.0') {
      if (req.headers.connection) {
        response.headers.connection = req.headers.connection
      } else {
        response.headers.connection = 'close'
      }
    } else if (!response.headers.connection) {
      if (req.headers.connection) { response.headers.connection = req.headers.connection }
      else {
        response.headers.connection = 'keep-alive'
      }
    }

    // Remove `Transfer-Encoding` header if client's protocol is HTTP/1.0
    // or if this is a DELETE request with no content-length header.
    // See: https://github.com/nodejitsu/node-http-proxy/pull/373
    if (req.httpVersion === '1.0' || (req.method === 'DELETE'
      && !req.headers['content-length'])) {
      delete response.headers['transfer-encoding'];
    }

    if ((response.statusCode === 301 || response.statusCode === 302)
      && typeof response.headers.location !== 'undefined') {
      location = url.parse(response.headers.location);
      if (location.host === req.headers.host) {
        if (self.source.https && !self.target.https) {
          response.headers.location = response.headers.location.replace(/^http\:/, 'https:');
        }
        if (self.target.https && !self.source.https) {
          response.headers.location = response.headers.location.replace(/^https\:/, 'http:');
        }
      }
    }

    //
    // When the `reverseProxy` `response` ends, end the
    // corresponding outgoing `res` unless we have entered
    // an error state. In which case, assume `res.end()` has
    // already been called and the 'error' event listener
    // removed.
    //
    var ended = false;
    response.on('close', function () {
      if (!ended) { response.emit('end') }
    });

    //
    // After reading a chunked response, the underlying socket
    // will hit EOF and emit a 'end' event, which will abort
    // the request. If the socket was paused at that time,
    // pending data gets discarded, truncating the response.
    // This code makes sure that we flush pending data.
    //
    response.connection.on('end', function () {
      if (response.readable && response.resume) {
        response.resume();
      }
    });

    response.on('end', function () {
      ended = true;
      if (!errState) {
        try { res.end() }
        catch (ex) { console.error("res.end error: %s", ex.message) }

        // Emit the `end` event now that we have completed proxying
        self.emit('end', req, res, response);
      }
    });

    // Allow observer to modify headers or abort response
    try { self.emit('proxyResponse', req, res, response) }
    catch (ex) {
      errState = true;
      return;
    }

    // Set the headers of the client response
    if (res.sentHeaders !== true) {
      Object.keys(response.headers).forEach(function (key) {
        res.setHeader(key, response.headers[key]);
      });
      res.writeHead(response.statusCode);
    }

    function ondata(chunk) {
      if (res.writable) {
        // Only pause if the underlying buffers are full,
        // *and* the connection is not in 'closing' state.
        // Otherwise, the pause will cause pending data to
        // be discarded and silently lost.
        if (false === res.write(chunk) && response.pause
            && response.connection.readable) {
          response.pause();
        }
      }
    }

    response.on('data', ondata);

    function ondrain() {
      if (response.readable && response.resume) {
        response.resume();
      }
    }

    res.on('drain', ondrain);
  });

  // allow unlimited listeners
  reverseProxy.setMaxListeners(0);

  //
  // Handle 'error' events from the `reverseProxy`. Setup timeout override if needed
  //
  reverseProxy.once('error', proxyError);

  // Set a timeout on the socket if `this.timeout` is specified.
  reverseProxy.once('socket', function (socket) {
    if (self.timeout) {
      socket.setTimeout(self.timeout);
    }
  });

  //
  // Handle 'error' events from the `req` (e.g. `Parse Error`).
  //
  req.on('error', proxyError);

  //
  // If `req` is aborted, we abort our `reverseProxy` request as well.
  //
  req.on('aborted', function () {
    reverseProxy.abort();
  });

  //
  // For each data `chunk` received from the incoming
  // `req` write it to the `reverseProxy` request.
  //
  req.on('data', function (chunk) {
    if (!errState) {
      var flushed = reverseProxy.write(chunk);
      if (!flushed) {
        req.pause();
        reverseProxy.once('drain', function () {
          try { req.resume() }
          catch (er) { console.error("req.resume error: %s", er.message) }
        });

        //
        // Force the `drain` event in 100ms if it hasn't
        // happened on its own.
        //
        setTimeout(function () {
          reverseProxy.emit('drain');
        }, 100);
      }
    }
  });

  //
  // When the incoming `req` ends, end the corresponding `reverseProxy`
  // request unless we have entered an error state.
  //
  req.on('end', function () {
    if (!errState) {
      reverseProxy.end();
    }
  });

  // Aborts reverseProxy if client aborts the connection.
  req.on('close', function () {
    if (!errState) {
      reverseProxy.abort();
    }
  });

  //
  // If we have been passed buffered data, resume it.
  //
  if (buffer) {
    return !errState
      ? buffer.resume()
      : buffer.destroy();
  }
};

exports.buffer = function (obj) {
  var events = [],
      onData,
      onEnd;

  obj.on('data', onData = function (data, encoding) {
    events.push(['data', data, encoding]);
  });

  obj.on('end', onEnd = function (data, encoding) {
    events.push(['end', data, encoding]);
  });

  return {
    end: function () {
      obj.removeListener('data', onData);
      obj.removeListener('end', onEnd);
    },
    destroy: function () {
      this.end();
        this.resume = function () {
          console.error("Cannot resume buffer after destroying it.");
        };

        onData = onEnd = events = obj = null;
    },
    resume: function () {
      this.end();
      for (var i = 0, len = events.length; i < len; ++i) {
        obj.emit.apply(obj, events[i]);
      }
    }
  };
};