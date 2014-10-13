#!/usr/bin/env python

import sys
import Image
import zbar
from netcatlib import *                                                                                                    

def readData(ncd): #{{{
    """read QR code, autoguesses size based on first line"""
    buf = ""
    while "\n" not in buf:
        buf += ncd.read_exact(1)

    size = len(buf) - 1
    print "Code of size %d" % size
    buf += ncd.read_exact((size+1) * (size-1))
    return buf.split("\n")[:size]
#}}}
def printData(argdata): #{{{
    print "\n".join(argdata)
#}}}
def flipRow(argdata, n): #{{{
    """flips all bits in a given row"""
    argarr = [list(x) for x in argdata]
    for row in range(len(argarr)):
	for col in range(len(argarr[0])):
	    if row == n:
	        argarr[row][col] = "+" if argarr[row][col] == "-" else "-"
	
    return ["".join(x) for x in argarr]
#}}}
def flipCol(argdata, n): #{{{
    """flips all bits in a given column"""
    argarr = [list(x) for x in argdata]
    for row in range(len(argarr)):
	for col in range(len(argarr[0])):
	    if col == n:
	        argarr[row][col] = "+" if argarr[row][col] == "-" else "-"
	
    return ["".join(x) for x in argarr]
#}}}
def fixColors(argdata): #{{{
    """invert entire image to make sure the top left corner has a - and not +"""
    # invert full image if colors are inverted
    refcolor = argdata[0][0]
    if refcolor == "+":
	for i in range(len(data)):
	    argdata = flipCol(argdata, i)
    return argdata
#}}}
def getQR(imgargrgb): #{{{
    """read QR code from image"""
    imgarg = imgargrgb.convert('L')
    # create a reader
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    # obtain image data
    width, height = imgarg.size
    raw = imgarg.tostring()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
	# do something useful with results
	print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
	return symbol.data

    # clean up
    del(image)
#}}}
def makeImage(argdata, c): #{{{
    """turn a code into an image, save it and display it"""
    size = len(argdata)
    img = Image.new( 'RGB', (size,size), "black") # create a new black image
    pixels = img.load() # create the pixel map
      
    for i in range(img.size[0]):    # for every pixel:
      for j in range(img.size[1]):
	  pixels[j,i] = (255,255,255) if argdata[i][j] == "+" else (0,0,0)
	       
    img = img.resize((size * 10,size * 10))
    #img.show()
    img.save("qrcode%d.png" % c)
    return img
#}}}
def correctQRv1(argdata): #{{{
    """correct the given QR code so that the positioning info and timing info are intact"""
    refcolor = argdata[0][0]
    print "reference color = %s" % refcolor

    size = len(argdata)

    # make sure first 1-7 columns have same color, positioning info
    for i in range(1,7):
	if argdata[0][i] != refcolor:
	    argdata = flipCol(argdata, i)

    if argdata[0][7] == refcolor:
	argdata = flipCol(argdata, 7)

    # fix timing info horizontal
    flipRefColor = True
    timingrow = 6
    for i in range(8,size - 8):
	if flipRefColor:
	    if argdata[timingrow][i] != refcolor:
		argdata = flipCol(argdata, i)
	else:
	    if argdata[timingrow][i] == refcolor:
		argdata = flipCol(argdata, i)
	flipRefColor = not flipRefColor

    # fix timing info vertical
    flipRefColor = True
    timingcol = 6
    for i in range(8,size - 8):
	if flipRefColor:
	    if argdata[i][timingcol] != refcolor:
		argdata = flipRow(argdata, i)
	else:
	    if argdata[i][timingcol] == refcolor:
		argdata = flipRow(argdata, i)
	flipRefColor = not flipRefColor

    # make sure last 7 columns have same color, positioning info
    if argdata[0][size - 8] == refcolor:
	argdata = flipCol(argdata, size - 8)

    for i in range(size - 7,size):
	if argdata[0][i] != refcolor:
	    argdata = flipCol(argdata, i)

    return argdata
#}}}

nc = Netcat('asis-ctf.ir', 12431)                                                                                             
nc.set_debuglevel(1)
nc.read_until("send \"START\"\n")
nc.write("START\n")

first = True
count = 1
while True:
    if count == 4:
	#nc.interact() #### Xor0x: uncomment this line
	pass
    if not first:
	nc.read_until("OK\n")
    else:
        first = False
    data = readData(nc)
    printData(data)
    data = correctQRv1(data)
    code = getQR(makeImage(fixColors(data), count))
    nc.write("%s\n" % code)
    count += 1


print "Done"
