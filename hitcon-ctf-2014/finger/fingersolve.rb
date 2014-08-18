#!/usr/bin/env ruby

require 'digest'
require 'timeout'
require 'socket'


begin
	s = TCPSocket.new '210.71.253.236', 7171
	loop do
		i = 0
		# get the first strings
		while i < 2 
			line = s.recv(1024)
			puts line
			i = i+1
		end
		# the hands
		hands = line.split("\"")
		hand1 = hands[1]
		hand2 = hands[3]
		hand3 = hands[5]
		#puts hand1
		#puts hand2
		#puts hand3

		# always go with hand2
		# 1 hand at a time
		n = "1\n"
		s.send n, 0

		# receive another line
		line = s.recv(1024)
		puts line

		# calculate the md5 and send the magic
		while hand2.size != 16
			hand2 = hand2 << "1"
		end
		#puts hand2

		ys = hand2.chars.each_slice(16).map(&:join)
      	md = ys.map{|y| Digest::MD5.hexdigest(y).to_i(16)}.inject(:+)
      	md = md.to_s << "\n"
      	#puts md
      	s.send md, 0

      	# receive another few lines
      	line = s.recv(1024)
		puts line
		line = s.recv(1024)
		puts line
		line = s.recv(1024)
		puts line
		line = s.recv(1024)
		puts line

		# check for opponents hand
		opponenthand = line.split(":")[1]
		opponenthand = opponenthand.split("show")
		opponenthand = opponenthand[0]
		opponenthand = opponenthand.strip()
		puts opponenthand
		if opponenthand.eql? hand3
			# we lost so we give the wrong secret
			s.send "1\n", 0
		else
			hand2 = hand2 << "\n"
			s.send hand2, 0
		end
	end
end