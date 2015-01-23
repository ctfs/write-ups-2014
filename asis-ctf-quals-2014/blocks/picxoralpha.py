from PIL import Image

# Picture is 19*19 pixels wide and 19*19 pixel high
img = Image.open('stego_100_f78a3acde659adf7ceef546380e49e5f')
m1 = m2 = ''

# Each 19x19 block represents 1 (white) or 0 (black)
for y in range(0, img.size[0], 19):
	for x in range(0, img.size[1], 19):
		r,g,b,a = img.getpixel((x,y))
		m1 += str(r & 1) # 

# Get the binary representation of the center 19x19 block
for y in range(171, 171 + 19):
	for x in range(171, 171 + 19):
		r,g,b,a = img.getpixel((x,y))
		m2 += str(a & 1)

# xor both
xor = ''.join(str(int(A)^int(B)) for A,B in zip(m1,m2))
# get the ascii representation of the binary stream
print ''.join(chr(int(xor[i:i+8], 2)) for i in range(0, len(xor), 8))
