#!/usr/bin/env python

import SocketServer
import SPI
import os
import binascii

PORT = 0xAE2
HOST = ""
BSIZE = 1024
FLAG = open("flag.txt").read()
PIN_CS = 34
KEY_ADDR = 0x23
DATA_ADDR = 0x22

class OnlineHardwareAES(SocketServer.BaseRequestHandler):

	def println(self, text):
		self.request.send(text + "\n")

	def help(self, param):
		for cmd in sorted(self.commands.keys()):
			if cmd is None:
				continue
			self.println("{} - {}".format(cmd.ljust(10), self.commands[cmd][1]))
	
	def set_key(self, param):
		key = param.decode("hex")
		if len(key) != 16:
			self.println("wrong key size")
			return
		self._set_key(key)
	
	def _set_key(self, key):
		return self.spi.write(KEY_ADDR, key)

	def get_key(self, param):
		self.println(self._get_key().encode("hex").strip())

	def _get_key(self):
		return self.spi.read(KEY_ADDR, 16)

	def encrypt(self, param):
		self.println(self._encrypt(param.decode("hex")).encode("hex").strip())

	def _encrypt(self, plaintext):
		result = ""
		p = len(plaintext)
		for i in xrange(0, len(plaintext), 16):
			text = plaintext[i:i + 16]
			if len(text) < 16:
				text += "\x00" * (16-len(text))
			result += self.spi.transceive(DATA_ADDR, text, 16)
		result += self.spi.transceive(DATA_ADDR, "\x00"*16, 16)
		return result[16:]

	def flag(self, paran):
		self._set_key(os.urandom(16))
		self.println(self._encrypt(FLAG).encode("hex").strip())

	def handle(self):
		# use minimal memory aes via spi
		self.spi = SPI.SPI(SPI.MODE1, PIN_CS)
		self.commands = {"help": (self.help, "show this help"),
				"setkey": (self.set_key, "Set AES key"),
				"getkey": (self.get_key, "Set AES key"),
				"encrypt": (self.encrypt, "Encrypt with AES"),
				"flag": (self.flag, "Encrypt flag"),
				}

		self.request.send("Welcome to the online AES encryption service\n")
		while True:
			cmdline = self.request.recv(BSIZE)
			if not cmdline:
				return
			cmdline = cmdline.strip().split(" ", 1)
			cmd = cmdline[0]
			param = ""
			if len(cmdline) > 1:
				param = cmdline[1]

			try:
				self.commands[cmd][0](param)
			except (KeyError,binascii.Error,TypeError):
				self.println("error")



class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":
	srv = ThreadedServer((HOST, PORT), OnlineHardwareAES)
	srv.allow_reuse_address = True
	srv.serve_forever()