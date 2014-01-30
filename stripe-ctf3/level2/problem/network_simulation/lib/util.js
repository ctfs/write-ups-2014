"use strict";

var crypto = require('crypto');

var sum = exports.sum = function (array) {
  return array.reduce(function (a, b) { return a + b; });
}

exports.average = function (array) {
  return sum(array) / array.length;
}

exports.sign = function (nonce, secret) {
  var hmacCreator = crypto.createHmac('sha256', secret);
  hmacCreator.update(nonce);
  return hmacCreator.digest('hex');
}

exports.hash = function (value) {
  var hashCreator = crypto.createHash('sha256');
  hashCreator.update(value);
  return hashCreator.digest('hex');
}

exports.generateRandom = function (byteCount) {
  var buf = crypto.randomBytes(byteCount);
  return buf.toString('hex');
}

exports.randString = function (randGenerator, length) {
  var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZ';
  length = length || 32;
  var string = '';
  var charIndex;
  var randomNumber;
  for (charIndex = 0; charIndex < length; charIndex++) {
    randomNumber = Math.floor(randGenerator() * chars.length);
    string += chars.substring(randomNumber, randomNumber + 1);
  }
  return string;
}