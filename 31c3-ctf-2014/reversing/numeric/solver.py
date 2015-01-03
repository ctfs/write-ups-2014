#!/usr/bin/env python2

def find_fraction(s):
	l = (0,1)
	r = (1,0)
	p = []
	while 1:
		m = (l[0]+r[0],l[1]+r[1])
		if s == m:
			break
		#s < p
		if s[0] * m[1] < m[0] * s[1]:
			p.append(0)
			r = m
		else:
			p.append(1)
			l = m
	return p[::-1]

def find_pos(p):
	r = 0
	for i in p:
		r *= 2
		r += i
	r += 1 << len(p)
	return r - 1

def get_path_for_num(num):
	path = []
	while num:
		num -= 1
		path.append(num & 1)
		num >>= 1
	return path[::-1]

def get_fraction(path):
	l = (0,1)
	r = (1,0)
	pos = 0
	while 1:
		m = (l[0]+r[0],l[1]+r[1])
		if pos >= len(path):
			break
		pos += 1
		if not path[-pos]:
			r = m
		else:
			l = m
	return m

def test():
	v = [1,1]
	for pos in xrange(1000):
		v.append(v[pos] + v[pos+1])
		v.append(v[pos+1])
		tmp1 = find_fraction((v[pos],v[pos+1]))
		tmp = find_pos(tmp1)
		tmp2 = get_path_for_num(pos)
		tmp3 = get_fraction(tmp2)
		#print pos, tmp, tmp1, tmp2, tmp3, (v[pos],v[pos+1])
		assert(pos == tmp)
		assert(tmp1 == tmp2)
		assert(tmp3 == (v[pos],v[pos+1]))
#test()
def str2num(s):
	n = 0
	for i, c in enumerate(s):
		n |= ord(c) << (i*8)
	return n
flag = "95be84a46f5d0b12f8a1524cb26d6ef0"
a,b = get_fraction(get_path_for_num(str2num(flag) + find_pos(find_fraction((23,42)))))
print "parameters for binary:", a,b
s = hex(find_pos(find_fraction((a,b))) - find_pos(find_fraction((23,42))))[2:-1].decode("hex")[::-1]
assert(s == flag)
print "solution would be:", s
