#!/usr/bin/env node

"use strict";

var crypto = require('crypto');
var fs = require('fs');
var http = require("http");
var nopt = require('nopt');
var url = require("url");

var util = require('./lib/util');

function respond(response, statusCode, contents) {
  response.writeHead(statusCode, {"Content-Type": "application/json"});
  if (contents) {
    response.write(JSON.stringify(contents));
  }
  response.end();
}

function respondError(response, responseCode, errorMessage) {
  var contents = {
    "error": errorMessage
  };
  respond(response, responseCode, contents);
}

var DownTime = function () {
  this.startTime = Date.now();
};
DownTime.prototype.end = function () {
  this.endTime = Date.now();
};
DownTime.prototype.duration = function () {
  var endTime = this.endTime || Date.now()
  return (endTime - this.startTime);
};

var QueueServer = function (responseDelay, allowedInFlight, maxQueueLength) {
  this.responseDelay = responseDelay;
  this.allowedInFlight = allowedInFlight;
  this.maxQueueLength = maxQueueLength;
  this.inFlight = 0;
  this.queued = [];
  this.downtimes = [];
};
QueueServer.prototype.pushRequest = function (value) {
  if (this.queued.length >= this.maxQueueLength) {
    respondError(reqData.response, "500", "Server is falling over from the load.");
  } else {
    this.queued.push(value);
  }
};
QueueServer.prototype.popRequest = function () {
  if (this.queued.length === 0) {
    this.inFlight -= 1;
    this.downtimes.push(new DownTime());
    return;
  }
  var value = this.queued[0];
  this.queued.splice(0, 1);
  this.handleRequest(value);
};
QueueServer.prototype.handleRequest = function (reqData) {
  if (reqData.closed) {
    process.nextTick(this.popRequest.bind(this));
    return;
  }
  var parsed = url.parse(reqData.request.url, true),
      nonce = parsed.query.nonce,
      contents,
      hmac;
  if (nonce === undefined) {
    respondError(reqData.response, "400", "No nonce was provided.");
    process.nextTick(this.popRequest.bind(this));
    return;
  }
  hmac = util.sign(nonce, this.secret);
  contents = {
    "hmac": hmac
  };
  setTimeout(this.waitAndRespond.bind(this), this.responseDelay, reqData, contents);
};
QueueServer.prototype.waitAndRespond = function (reqData, contents) {
  if (reqData.closed) {
    console.log("Client timed out while waiting for us.");
  } else {
    respond(reqData.response, 200, contents);
  }
  this.popRequest();
};

var RequestData = function (request, response) {
  this.request = request;
  this.response = response;
  this.closed = false;
};

function handleGET(queue, request, response) {
  var reqData = new RequestData(request, response);
  response.on('close', function () {
    reqData.closed = true;
  });
  if (queue.inFlight >= queue.allowedInFlight) {
    // Save this request for later
    queue.pushRequest(reqData);
  } else {
    // Handle now
    if (queue.downtimes.length != 0) {
      queue.downtimes[queue.downtimes.length - 1].end();
    }
    queue.inFlight += 1;
    queue.handleRequest(reqData);
  }
}

function handleHEAD(validPath, request, response) {
  var parsed = url.parse(request.url);
  if (parsed['pathname'] == "/" + validPath) {
    respond(response, 200);
  } else {
    respond(response, 400);
  }
}

function main() {
  var opts = {
    "secret": String,
    "in-socket": String,
    "in-port": String,
  };
  var parsed = nopt(opts),
      secret = parsed.secret || "defaultsecret",
      secretHash = util.hash(secret),
      listenTarget;

  if (parsed['in-socket'] !== undefined && parsed['in-port'] !== undefined) {
    console.log("Cannot specify both an in-port and an in-socket. Exiting.");
    process.exit(1);
  } else if (parsed['in-socket']) {
    listenTarget = parsed['in-socket'];
  } else {
    // Default: listen on port 3001
    listenTarget = parsed['in-port'] || '3001';
  }
  // Response delay in ms, Allowed in flight connections, Allowed queue length
  var queue = new QueueServer(75, 2, 4);
  queue.secret = secret;
  var server = http.createServer(function (request, response) {
    switch (request.method) {
    case "GET":
      handleGET(queue, request, response);
      break;
    case "HEAD":
      handleHEAD(secretHash, request, response);
      break;
    default:
      respondUserError(response, "Unsupported HTTP method " + request.method);
    }
  });

  server.on("listening", function () {
    if (parsed['in-socket'] !== undefined) {
      fs.chmodSync(parsed['in-socket'], "0666");
    }
  })

  console.log("The backend is up and listening.");
  server.listen(listenTarget);
}

main();
