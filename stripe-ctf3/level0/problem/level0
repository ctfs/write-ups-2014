#!/usr/bin/env ruby

# Our test cases will always use the same dictionary file (with SHA1
# 6b898d7c48630be05b72b3ae07c5be6617f90d8e). Running `test/harness`
# will automatically download this dictionary for you if you don't
# have it already.

path = ARGV.length > 0 ? ARGV[0] : '/usr/share/dict/words'
entries = File.read(path).split("\n")

contents = $stdin.read
output = contents.gsub(/[^ \n]+/) do |word|
  if entries.include?(word.downcase)
    word
  else
    "<#{word}>"
  end
end
print output
