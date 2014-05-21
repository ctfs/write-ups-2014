# DEF CON CTF Qualifier 2014: 3dttt

**Category:** Baby’s First
**Points:** 1
**Description:**

> Play well and play fast.
> `3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me:1234`

## Write-up

In this challenge you had to beat LegitBS’s bot in a game of 3D Tic-Tac-Toe. You had to get to a balance of +50 games.

Here is an example solution:

```python
import socket
import sys

def generate_combos():
  combos = []
  #all horizontal lines
  for grid in range(3):
    for row in range(3):
      combos.append([(0,row,grid), (1,row,grid), (2,row,grid)])

  for grid in range(3):
    for row in range(3):
      combos.append([(row,0,grid), (row,1,grid), (row,2,grid)])

  #all vertical lines
  for row in range(3):
    for col in range(3):
      combos.append([(row,col,0),(row,col,1),(row,col,2)])

  #les diagonnals in a same grid
  for grid in range(3):
    combos.append([(0,0,grid), (1,1,grid), (2,2,grid)])
    combos.append([(0,2,grid), (1,1,grid), (2,0,grid)])

  #diagonnals on the same plan
  for row in range(3):
    combos.append([(row,0,0), (row,1,1), (row,2,2)])
    combos.append([(0,row,0), (1,row,1), (2,row,2)])
    combos.append([(row,2,0), (row,1,1), (row,0,2)])
    combos.append([(0,row,2), (1,row,1), (2,row,0)])

  #diagonnal diagonnals?!
  combos.append([(0,0,0), (1,1,1), (2,2,2)])
  combos.append([(2,0,0), (1,1,1), (0,2,2)])
  combos.append([(0,2,0), (1,1,1), (2,0,2)])
  combos.append([(2,2,0), (1,1,1), (0,0,2)])

  return combos

def parse_board(data):

  my_moves = []
  his_moves = []
  all_moves = []

  lines = [line.strip() for line in data.split('\n') if line.find('|') != -1]
  clean_lines = [line.replace('0','') for line in lines]
  clean_lines = [line.replace('1','') for line in clean_lines]
  clean_lines = [line.replace('2','') for line in clean_lines]

  for idx, line in enumerate(clean_lines):
    if idx < 3:
      grid = 0
      row = idx
    elif idx < 6:
      grid = 1
      row = idx - 3
    else:
      grid = 2
      row = idx - 6
    cases = [case.strip() for case in line.split('|')]
    for idx, case in enumerate(cases):
      if case.find('X') != -1:
        my_moves.append((idx,row,grid))
        all_moves.append((idx,row,grid))
      elif case.find('O') != -1:
        his_moves.append((idx,row,grid))
        all_moves.append((idx,row,grid))
  return my_moves, his_moves, all_moves


def update_valid(combos, his_moves):
  for move in his_moves:
    for combo in combos:
      if move in combo:
        combos.remove(combo)

  return combos

def update_d_valid(combos, his_moves):
  for move in his_moves:
    for combo in combos:
      if move in combo:
        combos.remove(combo)

  return combos

def get_try(combos, my_moves, all_moves):

  best_count = 0
  best_combo = combos[0]
  for combo in combos:
    count = 0
    for move in my_moves:
      if move in combo:
        count +=1
    if count > best_count:
      best_count = count
      best_combo = combo

  for move in best_combo:
    if move not in all_moves:
      return move

  return None

def defensive_move(d_combos, his_moves, all_moves):

  danger_combo = []
  for combo in d_combos:
    count = 0
    for move in his_moves:
      if move in combo:
        count +=1
    if count == 2:
      danger_combo = combo

  for move in danger_combo:
    if move not in all_moves:
      return move

  return None

def get_try_apocalypse(used):

  for a in xrange(3):
    for b in xrange(3):
      for c in xrange(3):
        if (a,b,c) not in used:
          return (a,b,c)
  return None

HOST = '3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me'
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

my_moves = []
his_moves = []
all_moves = []
combos = generate_combos()
d_combos = generate_combos()

new_round = True

while True:
  try:

    data = s.recv(1024)
    if "flag" in data:
      print data
      break

    if new_round or data.find("Let's play again") != -1:
      my_moves = []
      his_moves = []
      all_moves = []
      combos = generate_combos()
      d_combos = generate_combos()

      s.send("1,1,1\n")
      s.recv(1024)
      my_moves, his_moves, all_moves = parse_board(data)
      # Best starter moves according to first google result!
      # Trustworthy source for sure
      if (1,1,0) in his_moves:
        s.send("1,1,2\n")
      else:
        s.send("1,1,0\n")
      new_round = False
      continue

    my_moves, his_moves, all_moves = parse_board(data)
    combos = update_valid(combos, his_moves)
    d_combos = update_d_valid(d_combos, my_moves)
    a_try = defensive_move(d_combos, his_moves, all_moves)

    # If no defensive moves are needed go offense
    if a_try is None:
      a_try = get_try(combos, my_moves, all_moves)

    # If can't find a good offensive move...
    # close your eyes and point somewhere >_<
    if a_try is None:
      a_try = get_try_apocalypse(all_moves)

    # (1, 1, 1) ---> 1,1,1
    s.send(str(a_try).replace('(','').replace(')','').replace(' ','')+'\n')

  except Exception as e:
    print e
    print "exception im very out"
    break
```

## Other write-ups

* (none yet)
