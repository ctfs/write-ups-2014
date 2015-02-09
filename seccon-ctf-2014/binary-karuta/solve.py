#!/usr/bin/env python
# coding=utf-8

from collections import defaultdict
import random
import logging
import nltk # pip install nltk
import time
import csv
import sys
import base64
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class ServerSession(object):
	uri = 'http://binkaruta.pwn.seccon.jp/cgi-bin/q.cgi'

	def __init__(self):
		self.binary = None
		self.architectures = []
		self.consecutive_wins = 0
		self.cookies = {}

	def _make_request(self, method='get', data=None):
		while True:
			try:
				if method == 'get':
					resp = requests.get(self.uri)
				else:
					resp = requests.post(self.uri, cookies=self.cookies, data=data)

				resp_data = resp.text.split(',')

				if resp_data[0] == 'wait':
					raise Exception('Rate Limit Exception')

				self.cookies.update(resp.cookies)
				self.architectures = resp_data[:7]
				self.binary = base64.b64decode(resp_data[7])
				self.consecutive_wins = int(resp_data[9])

				return resp_data
			except Exception, e:
				logger.error(e)
				logger.info('Waiting 60 seconds before next request')
				time.sleep(60)
				logger.info('Ignoring error and retrying request')

	def get_question(self):
		return self._make_request()

	def post_answer(self, architecture):
		answer = self.architectures.index(architecture) + 1
		return self._make_request(method='post', data={ 'A': answer })


class BinaryClassifier(object):

	def __init__(self, all_words):
		self._classifier = None
		self.all_words = all_words

	def _compute_features(self, binary):
		features = {}

		for word in self.all_words:
			features['contains(%s)' % bin(ord(word))] = (word in binary)

		return features

	def train(self, training_set):
		training_set = [(self._compute_features(binary), architecture)
			for binary, architecture in training_set]
		self._classifier = nltk.NaiveBayesClassifier.train(training_set)

	def accuracy(self, testing_set):
		testing_set = [(self._compute_features(binary), architecture)
			for binary, architecture in testing_set]
		return nltk.classify.accuracy(self._classifier, testing_set)

	def predict(self, binary, architectures):
		if self._classifier:
			arch_probs   = self._classifier.prob_classify(self._compute_features(binary))
			arch_probs   = [(arch, arch_probs.prob(arch)) for arch in arch_probs]
			architecture = reduce(lambda (a,b), (x,y): (x,y) if y > b else (a, b), arch_probs, (None, 0))
			return architecture
		else:
			return random.choice(architectures)

class BinaryDataStore(object):
	path = 'data.csv'

	def __init__(self):
		self._data_set = defaultdict(list)

		with open(self.path, 'r') as f:
			f = csv.reader(f)
			for row in f:
				self._data_set[row[0]].append(row[1])

	@property
	def words(self):
		all_words = set()
		for architecture, binaries in self._data_set.iteritems():
			for binary in binaries:
				for word in binary[::8]:
					all_words.add(word)
		return all_words

	@property
	def training_set(self):
		training_set = []
		for architecture, binaries in self._data_set.iteritems():
			break_point = int(len(binaries) * 0.8)
			for binary in binaries[:break_point]:
				training_set.append((architecture, binary))
		return training_set

	@property
	def testing_set(self):
		testing_set = []
		for architecture, binaries in self._data_set.iteritems():
			break_point = int(len(binaries) * 0.8)
			for binary in binaries[break_point:]:
				testing_set.append((architecture, binary))
		return testing_set

	def write(self, architecture, binary):
		self._data_set[architecture].append(binary)

		with open(self.path, 'a') as f:
			f.write('%s,%s\n' % (architecture, base64.b64encode(binary)))

	def __len__(self):
		return reduce(lambda x,y: x + len(self._data_set[y]), self._data_set, 0)


if __name__ == '__main__':

	dataset = BinaryDataStore()
	classifier = BinaryClassifier(dataset.words)
	session = ServerSession()
	session.get_question()

	while session.consecutive_wins <= 101:
		if len(dataset) and len(dataset) % 250 == 0:
			logger.info('Retraining classifier…')
			classifier = BinaryClassifier(dataset.words)
			classifier.train(dataset.training_set)
			logger.info('Cross-validating classifier…')
			logger.info('Classifier %s accurate.' %
						classifier.accuracy(dataset.testing_set))

		predicted_arch = classifier.predict(session.binary, session.architectures)
		last_binary = session.binary
		last_architectures = session.architectures

		resp = session.post_answer(predicted_arch)
		logger.info('Server responded with: %s' % resp)
		logger.info('Consecutive wins: %s' % session.consecutive_wins)

		correct_arch = last_architectures[int(resp[8]) - 1]

		dataset.write(correct_arch, last_binary)

		if predicted_arch == correct_arch:
			logger.info('Successfully classified %s' % correct_arch)
		else:
			# Reset Session
			logger.info('Failed. Prediction %s. Actual %s' % (predicted_arch, correct_arch))
			session = ServerSession()
			session.get_question()
