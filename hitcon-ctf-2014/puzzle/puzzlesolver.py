#!/usr/bin/env python
from PIL import Image
import sys

# write images
def write_im(j, data):
    name = str(j) + ".jpg"
    try:
        im = open(name,'wb')
        # add the end bytes
        data = data + "ffd9"
        im.write(data.decode('hex'))
        im.close()
    except:
        print("Something went wrong!")




# open image
with open("puzzle-81c5e9bdb219efbe4eb9b194fb33f7e6.jpg",'rb') as in_file:
     hex_data = in_file.read().encode('hex')

flag = True
# header string
head = "ffd8ffe000104a46494600010100000100010000"
# JFXX
jfxx = "4a46585800"
# start position
i = 22
j = 1
# get the data
while flag:
    length = hex_data[i*2:(i+2)*2]
    i2 = i+int(length,16)-2
    imhex = (head+hex_data[(i+10)*2:i2*2])
    i = i2+4
    write_im(j,imhex)
    j += 1
    jfcheck = hex_data[(i+2)*2:(i+7)*2]
    # no more jfxx thumbnails left
    if jfcheck != jfxx:
        flag = False

