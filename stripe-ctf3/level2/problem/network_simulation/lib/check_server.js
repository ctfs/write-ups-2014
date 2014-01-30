"use strict";

var http = require('http');
var underscore = require('underscore');

var checkServers = exports.checkServers = function (array, success, error) {
  var upCount = 0,
      errored = false,
      target,
      i;
  for (i = 0; i < array.length; i++) {
    check(
      array[i],
      function () {
        upCount += 1;
        if (upCount === array.length) {
          success();
        }
      },
      function () {
        if (errored === false) {
          errored = true;
          error();
        }
      }
    );
  }
}

var check = exports.check = function (connectionOptions, success, error) {
  var baseOptions = {
    path: "/",
    method: 'HEAD'
  };
  var options = underscore.extend(baseOptions, connectionOptions);
  var request = http.request(options, function (response) {
    response.on('data', function () {
      return;
    });
    response.on('end', function () {
      if (response.statusCode === 200) {
        console.log("Upstream server is up.");
        success();
      } else if (response.statusCode === 400) {
        console.log("400 response code. We may be using the wrong secret.");
        error();
      } else if (response.statusCode === 500) {
        console.log("500 response code. Shield may be failing to come up.");
        error();
      } else {
        console.log("Unexpected response code %s.", response.statusCode);
        error();
      }
    });
  });

  request.setTimeout(1000, function (socket) {
      console.log("Timeout checking backend. The backend is probably down.");
      request.abort();
  });

  request.on("error", function (err) {
    console.log("Error checking backend. The immediate upstream is probably down.");
    error();
  });

  request.end();
};

var checkWithBackoff = exports.checkWithBackoff = function (connectionOptions, success, failure, attempts, backoff) {
  var attempts,
      backoff = backoff || 500; // ms
  if (attempts === undefined) {
    attempts = 4;
  }
  console.log("Checking if backends are up.");
  var failedTry = function () {
    if (attempts >= 1) {
      // Try again, doubling the backoff time
      setTimeout(
        checkWithBackoff,
        backoff,
        connectionOptions,
        success,
        failure,
        attempts - 1,
        backoff * 2
      );
    } else {
      failure();
    }
  };
  check(connectionOptions, success, failedTry);
};