# DEF CON CTF Qualifier 2014: zombies

**Category:** Duchess
**Points:** 2
**Description:**

> Aim small, miss small. Or not...your call.
>
> `zombies_8977dda19ee030d0ea35e97ad2439319.2014.shallweplayaga.me 20689`

## Write-up

TODO: Add detailed challenge description

Here is a working example:

```python
import socket
import math
import numpy
import time

def parse_level(text):
  level = 0
  for line in text.split('\n'):
    if line.strip().startswith("Level"):
      levelline = line.strip().split()
      level = int(levelline[1])

  if level < 10:
    x,y = parse_level1(text)
  else:
    x,y = parse_level2(text)

  return x, y

def parse_level1(text):
  x = 0
  y = 0
  level = 0
  for line in text.split('\n'):
    if line.startswith("The zombie is stalking"):
      line = line.split()
      x = int(line[6].replace('m', ''))
      y = int(line[11].replace('m', ''))
      print "Zombie is at: "
      print "x: ", x
      print "y: ", y
  return x,y

def parse_level2(text):
  x = 0
  y = 0
  level = 0
  for line in text.split('\n'):
    if line.startswith("The zombie is stalking"):
      splitline = line.split()
      zx = int(splitline[14].replace('m', ''))
      zy = int(splitline[19].replace('m', ''))
      px = int(splitline[28].replace('m', ''))
      py = int(splitline[33].replace('m', ''))

      print "Zombie is at: "
      print "x: ", zx
      print "y: ", zy
      print "Puppy is at: "
      print "x: ", px
      print "y: ", py

    if line.find("eats the puppy") != -1:
      eta = int(line.split(' ')[2])
      print "ETA dead puppy:", eta

    if line.find("gone by") != -1:
      # Consider +1 because of the wait
      my_time = int(line.split(' ')[0]) + 1
      print "Elapsed time:", my_time + 1

  new_x, new_y = calculate_position(zx, zy, px, py, eta, my_time)
  dummy = s.recv(1024)
  print dummy
  return new_x,new_y

def calculate_angle(velocity, x, y):

  angle1 = None
  angle2 = None

  g = 9.80665
  root = math.sqrt( (velocity**4) - g*( (g * (x**2)) + (2 * y * (velocity**2)) ))
  print "G", x
  angle1 = numpy.arctan((velocity**2 + root) / (g*x))
  angle2 = numpy.arctan((velocity**2 - root) / (g*x))

  angle1 = 180 * angle1 / math.pi
  angle2 = 180 * angle2 / math.pi

  print "Calculated angles:"
  print "Angle1:", angle1
  print "Angle2:", angle2

  return angle1, angle2

def calculate_position(zx, zy, px, py, eta, mytime):

  distx = px - zx
  disty = py - zy

  ratio = float(mytime) / float(eta)

  new_x = (distx * ratio) + zx
  new_y = (disty * ratio) + zy

  print "new coords:", new_x, new_y

  return new_x, new_y

def shoot(angle, x, y, gun="r"):

  dump = ""
  if gun == 'r':
    dump += "r, "
    # I'm sorry...
    global rcpt
    rcpt += 1
    print "Riffle count: " ,rcpt
  else:
    dump += "p, "
    # I'm sorry...
    global pcpt
    pcpt += 1
    print "pistol count: ", pcpt
  angle = str(angle)
  dump += angle + ', '
  dump += str(x) +", "
  dump += str(y) + "\n"

  print "Sending:"
  print dump

  s.send(dump)
  data = s.recv(1024)
  print data
  return data


HOST = "zombies_8977dda19ee030d0ea35e97ad2439319.2014.shallweplayaga.me"
PORT = 20689

RIFFLE = "2\n"
PISTOL = "3\n"

riffle_velocity = 975
pistol_velocity = 375

rcpt = 0
pcpt = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

# intro
data = s.recv(1024)

# pick guns
s.send(RIFFLE)
data = s.recv(1024)
s.send(PISTOL)
data = s.recv(1024)
print data

#Game Start
while(True):
  # Need to sleep otherwise misses on gun changes
  # This needs to be accounted for in the zombie's position
  time.sleep(2)
  x, y = parse_level(data)
  # Hint said 50ish... not enough pistolling at 50ish
  if x < 55 and pcpt < 43:
    a1, a2 = calculate_angle(pistol_velocity, x, y)
    data = shoot(a2, x, y, gun='p')
  else:
    a1, a2 = calculate_angle(riffle_velocity, x, y)
    data = shoot(a2, x, y, gun='r')
  if data.lower().find("flag") != -1:
    break

s.close()
```

## Other write-ups and resources

* <http://sigint.ru/writeups/2014/05/19/defcon-2014-quals---zombies/>
* [Japanese](http://epsilondelta.hatenablog.jp/entry/2014/05/20/014011)
