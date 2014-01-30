#!/usr/bin/env node

"use strict";

var assert = require('assert');
var events = require('events');
var fs = require('fs');
var http = require('http');
var nopt = require('nopt');
var path = require('path');
var seedModule = require('seed-random');
var underscore = require('underscore');

var checkServer = require('./lib/check_server');
var util = require('./lib/util');

var Request = function (client, roundIndex, nonce) {
  this.client = client;
  this.simulation = client.simulation;
  this.roundIndex = roundIndex;
  this.nonce = nonce;
};

Request.prototype.log = function (message, force) {
  if (this.client.simulation.debugOutput || force) {
    console.log('Request[%s,%s]: %s',
      this.client.ip.slice(0, 8),
      this.nonce.slice(0, 8),
      message);
  }
};

Request.prototype.handleResponse = function (res, pageData) {
  var jsonResponse,
      hmac;
  if (res.statusCode !== 200) {
    this.log("Non-200 return code.");
    return;
  }
  try {
    jsonResponse = JSON.parse(pageData);
  } catch (err) {
    this.log("Could not parse response body.", true);
    return;
  }
  if (!jsonResponse.hmac) {
    this.log("Responded with no HMAC.", true);
    return;
  }
  hmac = util.sign(this.nonce, this.client.simulation.secret);
  if (hmac === jsonResponse.hmac) {
    this.simulation.registerSuccess(this.client, this.roundIndex, this.latency);
  } else {
    this.log("Responded with invalid HMAC", true);
  }
};

Request.prototype.run = function () {
  var self = this;
  var baseOptions = {
    path: '/?nonce=' + self.nonce,
    headers: {
      'X-Forwarded-For': self.client.ip
    }
  };
  var options = underscore.extend(self.client.simulation.connection, baseOptions);
  var startTime = Date.now();
  var req = http.get(options, function (res) {
    var pageData = "";
    res.on('data', function (chunk) {
      pageData += chunk;
    });

    res.on('end', function () {
      self.latency = Date.now() - startTime;
      self.handleResponse(res, pageData);
    });
  });

  req.on('socket', function (socket) {
    socket.setMaxListeners(0)
    socket.setTimeout(1000); // In ms
    socket.on('timeout', function () {
      self.log("Timeout. Aborting.");
      req.abort();
    });
  });

  req.on("error", function (e) {
    // Socket errors are expected when we our resources are small compared
    // to the traffic that we try to push through.
    self.log("Sword HTTP error: " + e.message);
  });
};

var Client = function (simulation, birthRound) {
  this.simulation = simulation;
  this.ip = simulation.randString(48);
  simulation.clients[this.ip] = this;
  this.birthRound = birthRound;
  this.lifetime = simulation.simulationParameters.clientLifetime;
  if (simulation.random() > simulation.simulationParameters.pElephant) {
    this.type = "mouse";
    this.delayUntilStart = simulation.random() * simulation.simulationParameters.roundLength;
    this.requestsPerRound = simulation.simulationParameters.mouseRequestsPerRound;
  } else {
    this.type = "elephant";
    this.delayUntilStart = (simulation.random() / 5) * simulation.simulationParameters.roundLength;
    this.requestsPerRound = simulation.simulationParameters.elephantRequestsPerRound;
  }
};

Client.prototype.expired = function (roundIndex) {
  return (this.lifetime <= roundIndex - this.birthRound);
};

Client.prototype.waitTime = function () {
  return this.simulation.simulationParameters.roundLength / this.requestsPerRound;
};

Client.prototype.runMouse = function (roundIndex) {
  var roundLength = this.simulation.simulationParameters.roundLength,
      waitBetweenRequests = (roundLength - this.delayUntilStart) / this.requestsPerRound;
  setTimeout(
    this.sendRequest.bind(this),
    this.delayUntilStart,
    0,
    roundIndex,
    waitBetweenRequests
  );
};

Client.prototype.runElephant = function (roundIndex) {
  var waitBetweenRequests = this.simulation.simulationParameters.roundLength / this.requestsPerRound;
  this.sendRequest(0, roundIndex, waitBetweenRequests);
};

Client.prototype.run = function (roundIndex) {
  switch (this.type) {
  case "mouse":
    this.runMouse(roundIndex);
    break;
  case "elephant":
    this.runElephant(roundIndex);
    break;
  default:
    assert(false, "Fell through cases.");
  }
};

Client.prototype.sendRequest = function (requestIndex, roundIndex, waitBetweenRequests) {
  var requestNonce = util.generateRandom(64);
  var request = new Request(this, roundIndex, requestNonce);
  request.run();
  var nextRequestIndex = requestIndex + 1;
  if (nextRequestIndex < this.requestsPerRound) {
    setTimeout(
      this.sendRequest.bind(this),
      waitBetweenRequests,
      nextRequestIndex,
      roundIndex,
      waitBetweenRequests
    );
  }
};

var Simulation = function (seed, simulationParameters) {
  this.simulationParameters = simulationParameters;
  this.random = seedModule(seed);
  this.simulationResults = [];
  this.responseTotal = 0;
  this.clients = {};
  this.currentRound = -1;
  this.roundStartTimes = [];
};

Simulation.prototype.randString = function (length) {
  return util.randString(this.random, length);
};

Simulation.prototype.duration = function () {
  return this.simulationParameters['roundLength'] * this.simulationParameters['roundCount'];
};

Simulation.prototype.runSimulation = function (clients) {
  if (clients === undefined) {
    clients = [];
  }
  var roundIndex = ++this.currentRound;
  var i;
  var client;

  this.roundStartTimes[roundIndex] = Date.now();
  this.simulationResults[roundIndex] = [];

  var runningClients = [];
  // Create clients to replace any that have expired
  for (i = 0; i < clients.length; i++) {
    client = clients[i];
    if (!client.expired(roundIndex)) {
      runningClients.push(client);
    }
  }
  var clientsToCreate = this.simulationParameters.clientsPerRound - runningClients.length;
  for (i = 0; i < clientsToCreate; i++) {
    client = new Client(this, roundIndex);
    runningClients.push(client);
  }
  // Run the clients
  for (i = 0; i < runningClients.length; i++) {
    runningClients[i].run(roundIndex);
  }
  if (roundIndex + 1 >= this.simulationParameters.roundCount) {
    setTimeout(
      this.scoreSimulation.bind(this),
      this.simulationParameters.roundLength
    );
  } else {
    setTimeout(
      this.runSimulation.bind(this),
      this.simulationParameters.roundLength,
      runningClients
    );
  }
};

Simulation.prototype.registerSuccess = function (client, roundIndex, latency) {
  this.responseTotal += 1;
  if (client.type === "elephant") {
    // No points for elephants!
    return;
  }
  var mouseCount = this.simulationResults[roundIndex][client.ip] || 0;
  this.simulationResults[roundIndex][client.ip] = mouseCount + 1;
  this.maxLatency = this.maxLatency ? Math.max(this.maxLatency, latency) : latency;
};

Simulation.prototype.scoreRound = function (roundResults) {
  console.log("Round");
  var score = 0;
  var self = this;
  Object.keys(roundResults).forEach(function (ip) {
    var successes = roundResults[ip];
    var client = self.clients[ip];
    console.log("IP %s (%s): %d", ip.slice(0, 8), client.type, successes);
    score += successes;
  });
  if (score == 0) {
    console.log("No mice got through this round.");
  }
  return score;
};

Simulation.prototype.calculateDowntime = function (responseCount) {
  // Calculate the number of additional requests that could have been handled
  var totalTime = this.simulationParameters['backendCount'] * this.simulationParameters['backendInFlight'] * this.duration(),
      potentialResponses = totalTime / this.simulationParameters['backendProcessingTime'];
  return potentialResponses - responseCount;
}

Simulation.prototype.scoreSimulation = function () {
  console.log("Scoring now");
  var resultsPath = this.resultsPath,
      roundScores = this.simulationResults.map(this.scoreRound.bind(this)),
      goodCount = util.sum(roundScores),
      backendDeficit = this.calculateDowntime(this.responseTotal);

  var output = {
    "good_responses": goodCount,
    "backend_deficit": backendDeficit,
    "correct": true
  };
  console.log("Number of total responses %s", this.responseTotal)
  console.log("Number of good responses: %s", goodCount);
  console.log("Number of responses less than ideal: %s", backendDeficit);
  fs.writeFileSync(resultsPath, JSON.stringify(output));
  process.exit();
};

function main() {
  var opts = {
    "secret": String,
    "out-socket": String,
    "out-port": String,
    "check-server": Boolean,
    "debug": Boolean,
    "results-path": String,
    "run-time": Number
  };
  var parsed = nopt(opts),
      resultsPath = parsed['results-path'] || path.resolve(__dirname, "results.json"),
      secret = parsed.secret || "defaultsecret",
      secretHash = util.hash(secret),
      connectionOptions,
      seed,
      simulationParameters;

  if (parsed['out-socket'] !== undefined && parsed['out-port'] !== undefined) {
    console.log("Cannot specify both an out-port and an out-socket. Exiting.");
    process.exit(1);
  } else if (parsed['out-socket']) {
    connectionOptions = {'socketPath': parsed['out-socket']};
  } else {
    connectionOptions = {
      'host': 'localhost',
      'port':  parsed['out-port'] || '3000'
    };
  }
  connectionOptions['path'] = "/" + secretHash;

  if (parsed.argv.remain.length > 1) {
    console.log("Expected at most one extra arg and received more. Exiting.");
  }
  seed = parsed.argv.remain[0] || util.generateRandom(32);
  console.log("Using seed %s", seed);

  simulationParameters = {
    'clientLifetime': 2, // In rounds
    'roundLength': 500, // In ms
    'roundCount': 40,
    'clientsPerRound': 5,
    'pElephant': 0.4,
    'mouseRequestsPerRound': 2,
    'elephantRequestsPerRound': 50,
    'backendCount': 2,
    'backendInFlight': 2,
    'backendProcessingTime': 75
  };

  if (parsed['run-time']) {
    simulationParameters.roundCount = Math.floor(
      parsed['run-time'] * 1000 / simulationParameters.roundLength);
  }

  var simulation = new Simulation(seed, simulationParameters);
  simulation.connection = connectionOptions;
  simulation.resultsPath = resultsPath;
  simulation.debugOutput = parsed['debug'];
  simulation.secret = secret;

  checkServer.checkWithBackoff(
    connectionOptions,
    function () {
      if (parsed['check-server']) {
        // Just check that the server is up.
        console.log("Server is up.");
        process.exit(0);
      } else {
        simulation.runSimulation();
      }
    },
    function () {
      console.log("Server is not up. Exiting.");
      process.exit(1);
    }
  );
}

main();
