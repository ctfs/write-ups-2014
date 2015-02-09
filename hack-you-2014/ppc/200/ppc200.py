#!/usr/bin/python
from random import randint
from termcolor import colored
from time import time
import re
import SocketServer

FLAG = 'CTF{0a10f3f9e37d18c39e017ec8bbd5d2ea}'
TIME_LIMIT = 5.0

class Game:
	def __init__(self, n = 20, m = 10):
		self.n = n
		self.m = m
		self.map = [[None for i in xrange(self.m)] for j in xrange(self.n)]
		self.k = 0.5
		self.colors = {1:'green',2:'red',3:'yellow',4:'blue',5:'cyan',6:'white'}
		self.max_cnt = 20
		self.point_num = 0
		self.curr = None
		self.status = 0
		#0  - in game
		#1  - error
		#2  - time limit
		#3 - win
		self.Generate()
		self.start = time()

	def RandomPoint(self):
		return (randint(0, self.n-1), randint(0, self.m-1))

	def GetStatus(self):
		return self.status

	def Colorize(self, a, b, c):
		self.map[a[0]][a[1]] = c
		self.map[b[0]][b[1]] = c
		self.point_num += 2

	def Free(self, p):
		return (0 <= p[0] < self.n and 0 <= p[1] < self.m and self.map[p[0]][p[1]] == None)

	def Generate(self):
		while self.point_num < self.n * self.m * (1.0 - self.k):
			p1 = self.RandomPoint()
			p2 = self.RandomPoint()
			color = randint(1,6)
			if p1 != p2 and self.Free(p1) and self.Free(p2):
				if p1[0] != p2[0] and p1[1] != p2[1]:
					p_a = (p2[0],p1[1])
					p_b = (p1[0],p2[1])
					if self.Free(p_a) or self.Free(p_b):
						self.Colorize(p1, p2, color)
				else:
					if p1[0] == p2[0]:
						for dy in xrange(min(p1[1],p2[1])+1, max(p1[1],p2[1])):
							if self.Free((p1[0], dy)):
								self.Colorize(p1, p2, color)
								break
					elif p1[1] == p2[1]:
						for dx in xrange(min(p1[0], p2[1])+1, max(p1[0],p2[0])):
							if self.Free((dx, p1[1])):
								self.Colorize(p1, p2, color)
								break

	def Checker(self, data):
		if time() - self.start >= TIME_LIMIT:
			self.status = 2
			return
		arr = re.findall('\((\d+),(\d+)\)', data, re.DOTALL)
		arr = map(lambda x : (int(x[0]), int(x[1])), arr)
		d = [(0, -1), (-1, 0), (0, 1), (1, 0)]
		for p in arr:
			self.curr = p
			i,j = p
			if self.Free((i,j)):
				points = {}
				for di, dj in d:
					num = 1
					while 0 <= i+num*di < self.n and 0 <= j+num*dj < self.m:
						if not self.Free((i+num*di,j+num*dj)):
							c = self.map[i+num*di][j+num*dj]
							if c in points.keys():
								points[c].append((i+num*di,j+num*dj))
							else:
								points[c] = [(i+num*di,j+num*dj)]
							break
						num += 1
				#process
				for k,v in points.items():
					if len(v) > 1:
						for element in v:
							self.map[element[0]][element[1]] = None
							self.point_num -= 1
				#check for end
				if self.point_num == 0:
					self.status = 3
					break 
			else:
				self.status = 1
				break


	def Output(self):
		ret = ''
		ret += ' ' * 3 + ''.join(['%s' % i for i in xrange(10)]) + '\n'
		ret += ' ' * 2 + '-' * 11 + '\n'
		for t,row in enumerate(self.map):
			num = ('%s|' % t).rjust(3, ' ')
			ret += '%s%s\n' % (num, ''.join([' ' if a == None else colored('0', self.colors[a]) for a in row]))
		ret += '#' * 13 + '\n'
		return ret

class MyHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		req = self.request
		req.sendall('Welcome to ColorMatch game!\nClick on the connect point of same color blocks in empty area to eliminate them.\nIt also means the nearest blocks to connect point, either in horizontal or vertical direction, will be elimanted if they are the same color.\nSend your moves in this format (x1,y1);(x2,y2);...(xn,yn)\n')
		obj = Game()
		while obj.GetStatus() == 0:
			req.sendall(obj.Output())
			data = req.recv(65535)
			obj.Checker(data)
		code = obj.GetStatus()
		if code == 1:
			req.sendall('Wrong move - (%s,%s)\n' % (obj.curr[0], obj.curr[1]))
		elif code == 2:
			req.sendall('You are too slow...\n')
		elif code == 3:
			req.sendall('You win!\n%s\n' % FLAG)
		req.close()

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":
   HOST, PORT = "", 9876
   server = ThreadedServer((HOST, PORT), MyHandler, False)
   server.allow_reuse_address = True
   server.server_bind()
   server.server_activate()
   server.serve_forever()

