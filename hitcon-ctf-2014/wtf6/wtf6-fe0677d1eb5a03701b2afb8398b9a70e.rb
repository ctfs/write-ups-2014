#!/usr/bin/env ruby

require 'digest'
require 'timeout'

def md5(s)
  Digest::MD5.hexdigest(s)
end

def sha1(s)
  Digest::SHA1.hexdigest(s)
end

def wtf6(s)
  md5(s)[0..15] + sha1(s)[-16..-1]
end

def mix(a, b)
  a.bytes.zip(b.bytes).map{|x, y| ((x + y) & 0xFF).chr}.join
end

$stdin.binmode
$stdout.sync = true

begin
  Timeout::timeout(10) do
    puts 'Hi :)'
    a = gets.chomp
    b = gets.chomp

    p [md5(a), sha1(a), wtf6(a)]
    p [md5(b), sha1(b), wtf6(b)]

    if a == b
      puts 'too easy, huh?'
      exit
    end

    unless a.end_with?('HITCON') and b.end_with?('HITCON')
      puts "The strings must end with..."
      puts <<-'HITCON'
        ___                       ___           ___           ___           ___     
       /\__\          ___        /\  \         /\  \         /\  \         /\__\    
      /:/  /         /\  \       \:\  \       /::\  \       /::\  \       /::|  |   
     /:/__/          \:\  \       \:\  \     /:/\:\  \     /:/\:\  \     /:|:|  |   
    /::\  \ ___      /::\__\      /::\  \   /:/  \:\  \   /:/  \:\  \   /:/|:|  |__ 
   /:/\:\  /\__\  __/:/\/__/     /:/\:\__\ /:/__/ \:\__\ /:/__/ \:\__\ /:/ |:| /\__\
   \/__\:\/:/  / /\/:/  /       /:/  \/__/ \:\  \  \/__/ \:\  \ /:/  / \/__|:|/:/  /
        \::/  /  \::/__/       /:/  /       \:\  \        \:\  /:/  /      |:/:/  / 
        /:/  /    \:\__\       \/__/         \:\  \        \:\/:/  /       |::/  /  
       /:/  /      \/__/                      \:\__\        \::/  /        /:/  /   
       \/__/                                   \/__/         \/__/         \/__/    
      HITCON
      exit
    end

    if wtf6(a) != wtf6(b)
      print "$ "
      gets
      puts "WTF? This is NOT shell, just one dollar!"
      exit
    end

    eval mix(a, b)
  end
rescue Timeout::Error
  puts "Why are you so slow?!"
end
