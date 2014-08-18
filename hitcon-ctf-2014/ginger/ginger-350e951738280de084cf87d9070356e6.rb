#!/usr/bin/env ruby

require 'digest'
require 'timeout'

class String
  def red
    "\e[1;31m#{self}\e[0m"
  end

  def green
    "\e[1;32m#{self}\e[0m"
  end

  def yellow
    "\e[1;33m#{self}\e[0m"
  end
end

class Integer
  def bar()
    n = self / 5
    "[#{('|' * n).ljust(20)}] #{self.to_s.ljust(3)} / 100"
  end
end

$stdout.sync = true

boss_hp = 100
your_hp = 100
round   = 0

begin
  Timeout.timeout(600) do
    loop do
      round += 1
      hands = 3.times.map{rand(1..36**5).to_s(36)}

      puts "======================= Round #{round} ========================"
      puts "boss hp = #{boss_hp.bar.green}"
      puts "your hp = #{your_hp.bar.red}"
      puts "hands   = #{hands.inspect}"
      puts

      print "how many? "
      n = gets.to_i

      print "the magic? "
      m = gets.to_i

      x = hands.sample
      5.times do
        sleep 0.2
        print '.'
      end
      puts "here is mine: #{x}"

      print "show me the secret: "
      ys = gets.chomp

      if ys.size != 16 * n
        puts "hey, length should be #{16 * n}!".yellow
        exit
      end

      ys = ys.chars.each_slice(16).map(&:join)

      if ys.map{|y| Digest::MD5.hexdigest(y).to_i(16)}.inject(:+) != m
        puts "DO NOT CHEAT!!!!".yellow
        exit
      end

      ys = ys.map{|y| hands.find{|h| y.start_with?(h)}}

      if ys.include?(nil)
        puts "O_________O??".yellow
        exit
      end

      y = hands.max_by{|h| ys.count(h)}
      xi = hands.index(x)
      yi = hands.index(y)

      if xi == (yi + 1) % 3
        atk = rand(30..60)
        your_hp -= atk
        puts "you lose and your hp -= #{atk} ^_<".red
      elsif xi == (yi - 1) % 3
        atk = rand(1..2)
        boss_hp -= atk
        puts "!#^%*^&!@##...boss hp -= #{atk} QQ".green
      else
        puts "uhh, nothing happened"
      end

      if your_hp <= 0
        puts "you died lalalala ~~".red
        exit
      end

      if boss_hp <= 0
        puts "gg.".green
        puts IO.read('flag').reverse
        exit
      end
    end
  end
rescue Timeout::Error => e
  puts
  puts
  puts "Boss is going home (wave".red
end
