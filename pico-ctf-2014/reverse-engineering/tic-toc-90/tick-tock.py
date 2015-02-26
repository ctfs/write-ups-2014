#!/usr/bin/env python
import math
import time
import sys

def clock(n,m):
  '''for display purposes only'''
  c = [bytearray(" "*(42+len(str(n)))) for _ in xrange(21)]

  for x in xrange(21):
    for y in xrange(21):
      if (((x-10)**2 + (y-10)**2) > 90) and (((x-10)**2 + (y-10)**2) < 110):
        c[y][2*x] = '.'

  for i in xrange(11):
    xcoord = int(10+round(i*math.sin(2*(n%m)*math.pi/m)))
    ycoord = int(10-round(i*math.cos(2*(n%m)*math.pi/m)))
    c[ycoord][2*xcoord] = 'O'
    if i == 10:
      c[ycoord][2*xcoord+1:2*xcoord+3+len(str(n))] = " "+str(n)+" "

  return c

def printc(c,msg=""):
  print '\033[0;0H'+msg
  print
  for cl in c:
    print str(cl)

def count(n,m,msg=""):
  # n % m
  spin_for = min((m*10),n)
  nspots = 112
  for i in xrange(0,spin_for,m/nspots+1):
    speed = 1.0/((spin_for-i)/(m/nspots+1)+1)
    printc(clock(1+i+n-spin_for,m),msg)
    time.sleep(speed)
  if m/nspots+1 > 2:
    for j in xrange(i,spin_for,max((spin_for-i)/50,1)):
      printc(clock(1+j+n-spin_for,m),msg)
  printc(clock(n,m),msg)
  return n%m

def powmod(n,p,m,msg=""):
  # n^p % m
  for i in xrange(max(0,p-100),p+1):
    speed = 1.0/math.sqrt(1+p-i)
    printc(clock(pow(n,i,m),m),msg)
    time.sleep(speed)
  return pow(n,p,m)


if len(sys.argv) < 3:
  print "Usage: %s password signature"%sys.argv[0]
  sys.exit(0)

num = int(sys.argv[1])
if num > 10000000000000000000000000000000000000000000000000000000:
  print "that's a really really really big number"
  sys.exit(0)

#num2 is just given as an integer
num2 = int(sys.argv[2])
if num2 <= 1:
  print "that's a really small number"
  sys.exit(0)
if num2 >= 40000000000:
  print "that's a pretty big number"
  sys.exit(0)

secretz = [(1, 2), (2, 3), (8, 13), (4, 29), (130, 191), (343, 397), (652, 691), (858, 1009),
           (689, 2039), (1184, 4099), (2027, 7001), (5119, 10009), (15165, 19997), (15340, 30013),
           (29303, 70009), (42873, 160009), (158045, 200009)]

print '\033[2J'

for (r,m) in secretz:
  if count(num,m,"%d %% %d"%(num,m)) != r:
    print
    print "%d %% %d != %d... WRONG"%(num,m,r)
    sys.exit(0)
  else:
    print
    print "%d %% %d == %d... GOOD"%(num,m,r)
    time.sleep(2)
    print '\033[2A'
    print " "*90

print "You have the first part, but how about this:"
time.sleep(2)
print '\033[2J'

if powmod(num,num2,200009*160009,"%d ^ %d %% %d"%(num,num2,200009*160009)) != 1:
  print
  print "%d ^ %d %% %d != 1... WRONG"%(num,num2,200009*160009)
  sys.exit(0)
else:
  print "Congratulations! The flag is: %s_%s"%(sys.argv[1],str(num2))
