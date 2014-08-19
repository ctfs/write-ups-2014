#!/usr/bin/env python
from PIL import Image
import sys




# put all the images in the new image
def loop_im(new_im):
    for i in range(100):
        name = str(i+1) + ".jpg"
        im = Image.open(name)
        new_im.paste(im, ((i%10)*128,i/10*96))
# put all the images in the new image
def solve_im(new_im, arr):
    for i in range(100):
        name = str(i+1) + ".jpg"
        im = Image.open(name)
        new_im.paste(im, ((arr.index(i)%10)*128,arr.index(i)/10*96))

# our initial image
puzzle1 = Image.new('RGB', (1280,960))
loop_im(puzzle1)
puzzle1.show()

# the image created by the array
puzzle2 = Image.new('RGB', (1280,960))
aIm = [61,51,15,72,26,52,75,85,96,83,84,56,8,49,35,46,63,81,66,10,98,29,71,23,58,67,43,18,79,24,7,60,99,31,25,20,70,73,82,74,69,14,91,12,45,65,62,4,28,48,32,87,9,54,95,53,47,78,36,11,5,88,97,1,0,30,42,64,89,21,55,2,38,22,19,40,93,34,94,77,50,16,68,41,80,59,86,44,57,92,39,13,90,6,76,17,3,33,27,37]
solve_im(puzzle2, aIm)
puzzle2.show()
puzzle2.save("puzzlesolved.bmp")
