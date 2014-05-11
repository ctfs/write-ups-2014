#!/usr/bin/env python

import Image
import random
import sys

def get_color(x, y, r):
	n = (pow(x, 3) + pow(y, 3)) ^ r
	return (n ^ ((n >> 8) << 8 ))

flag_img = Image.open("enc.png")
im = flag_img.load()

for r in range(256):
    print "Trying key %d" % r
    enc_img = Image.new(flag_img.mode, flag_img.size)
    enpix = enc_img.load()

    for x in range(flag_img.size[0]):
	    for y in range(flag_img.size[1]):
		    if get_color(x, y, r) == im[x,y]:
			enpix[x,y] = 0
		    else:
			enpix[x,y] = 255
		    

    enc_img.save('decoded_%d.png' % r)
