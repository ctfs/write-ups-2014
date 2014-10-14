#!/usr/bin/env python
# coding=utf-8

import cv2
import cv2.cv
import numpy as np
from PIL import Image
import cookielib, urllib2
import re
from threading import Thread
from multiprocessing import Process, Value, Lock
import time

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

level = 0
def init_page():
	global opener, level
	result = opener.open('http://asis-ctf.ir:12443/').read()
	p = re.compile(ur'<p class="level"><b>level ([0-9]{1,2})')
	level = int(re.findall(p, result)[0])
	print "Running level %i" % level
	print cj

def get_circle_color(img_name):
	img = cv2.imread(img_name)
	output = img.copy()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	a = np.array([])
	circle = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 50, a, 50, 5)[0][0]

	x = circle[0]
	y = circle[1]

	im = Image.open(img_name)
	rgb_im = im.convert('RGB')
	t = (int(x),int(y))
	return rgb_im.getpixel(t)

def download(pic):
	global opener
	a = opener.open("http://asis-ctf.ir:12443/pic/%i" % pic).read()
	f = open("%i.png" % pic, "wb")
	f.write(a)
	f.close()

def send_pair(pic):
	url = "http://asis-ctf.ir:12443/send?first=%i&second=%i" % (pair[0], pair[1])
	result = opener.open(url).read()
	print result
	dec_counter()



lock = Lock()
counter = 0
done_recv = False
def inc_counter():
	global lock, counter
	with lock:
		counter += 1

def dec_counter():
	global lock, counter
	with lock:
		counter -= 1

def download_and_process(pic):
	download(pic)
	dec_counter()


while level <= 40:
	init_page()
	done_recv = False
	counter = 0

	for pic in range(0,16):
		inc_counter()
		thread = Thread(target = download_and_process, args = (pic, ))
		thread.start()

	while counter > 0:
		time.sleep(0.1)

	colors = []
	for pic in range(0, 16):
		colors.append(get_circle_color("%i.png" % pic))

	pairs = []

	for i in range(0, 16):
		smallest = 0xffff
		match = i
		for j in range(i+1,16):
			x = np.sum(np.abs(np.subtract(colors[i], colors[j])))
			if x < smallest:
				smallest = x
				match = j
		if smallest < 100:
			pairs.append((i,match))

	counter = 0
	for pair in pairs:
		inc_counter()
		thread = Thread(target = send_pair, args = (pair, ))
		thread.start()

	while counter > 0:
		time.sleep(0.1)

print opener.open('http://asis-ctf.ir:12443/flag').read()
