#!/usr/bin/env python
# coding=utf-8

import requests

samples = 0
with open('data.csv', 'w') as f:
	while samples < 7000:
		resp = requests.get('http://binkaruta.pwn.seccon.jp/cgi-bin/q.cgi')
		print 'samples collected %d' % samples

		data = resp.text.split(',')

		if data[0] == 'wait':
			continue

		architectures = data[:7]
		binary = data[7]

		for arch in architectures:
			f.write('%s,%s\n' % (arch, binary))
			samples += 1
