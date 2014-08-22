import os
import sys
import hashlib
import random
import string
import socket
import json
import time
import multiprocessing
import signal

s = socket.socket()

host = '210.71.253.236'
port = 7979

TOP_LEVEL=16
OPTION_COUNT=1
ALLOW_SUBOPTIMAL=True

print "TOP_LEVEL=%d OPTION_COUNT=%d  ALLOW_SUBOPTIMAL=%s" % (TOP_LEVEL, OPTION_COUNT, ALLOW_SUBOPTIMAL)

s.connect((host, port))

s.settimeout(0.1)

def make_hashes(prefix):
    l = 16-len(prefix)
    while True:
        s = "".join([random.choice(string.letters + string.digits) for i in range(l)])
        yield (prefix + s, hashlib.md5(prefix + s).hexdigest())

class MakeOptions(object):
    def __init__(self, prefix):
        super(MakeOptions, self).__init__()
        self.data = []
        self.prefix = prefix
        for i in range(17):
            # Each level is digits: (hashsum, [list of (string, hash) pairs])
            self.data.append({})
        self.options = {}

    def collapse(self, lst):
        if isinstance(lst[0], tuple):
            return self.collapse(lst[0]) + self.collapse(lst[1])
        else:
            return (lst[0][0],lst[1][0])

    def insert(self, level, hashsum, hashsumtxt, lst):
        if level == TOP_LEVEL:
            if (hashsumtxt, 2**TOP_LEVEL) not in self.options:
                 lst = self.collapse(lst)
                 self.options[(hashsumtxt, len(lst))] = lst
            return
        n = int(hashsumtxt[-level*2-2:][:2], 16)
        if (256-n) in self.data[level]:
            oldhashsum, oldlst = self.data[level][256-n]
            newhashsum = oldhashsum + hashsum
            t = newhashsum >> (128-16+level+1)
            if (-32678) <= (t-32768)<<(level) < (32768):
                newhashsumtxt = "%X" % newhashsum
                self.insert(level+1, newhashsum, newhashsumtxt, (oldlst, lst))
        self.data[level][n] = (hashsum, lst)

    def run(self):
        self.hashes = 0
        for s, h in make_hashes(self.prefix):
            self.hashes += 1
            if int(h[0],16) < 6 or int(h[0],16) > 9:
                continue
            self.insert(0, int(h, 16), h, [(s,h)])
            if len(self.options) >= OPTION_COUNT:
                break
        return self.options

def make_options(hand):
    return MakeOptions(hand).run()

def write_stats():
    data = dict(pid = os.getpid(),
                time = time.time() - start_time,
                hits = hits,
                draws = draws,
                found_optimal = found_optimal,
                found_optimal_loops = found_optimal,
                found_suboptimal = found_suboptimal,
                found_suboptimal_loops = found_suboptimal_loops,
                tot_upload = tot_upload,
                tot_loops = tot_loops,
                top_level = TOP_LEVEL,
                option_count = OPTION_COUNT,
                allow_suboptimal = ALLOW_SUBOPTIMAL,)
    
    with open("finger.stats.txt","a") as f:
        json.dump(data, f)
        f.write("\n")

keep_going = True
def quit(*args, **kwargs):
    global keep_going
    keep_going = False
    
signal.signal(signal.SIGINT, quit)

start_time = time.time()
hits = 0
draws = 0
found_optimal = 0
found_optimal_loops = 0
found_suboptimal = 0
found_suboptimal_loops = 0
tot_loops = 0
tot_upload = 0
                        
pool = multiprocessing.Pool(4)

buf = ""
while keep_going:
    if '\n' in buf or buf.endswith(':'):
        l, _, buf = buf.partition('\n')
    else:
        try:
            buf += s.recv(1000)
            continue
        except socket.timeout:  # On timeout process anyway
            if not buf:
                continue

            l = buf
            buf = ''
            pass

    print l

    if '====' in l:
        print ">>> Time so far: %.1f minutes hits %d draws %d" % ((time.time() - start_time)/60, hits, draws)
        if hits > 0:
            print ">>> Est total time: %.1f minutes" % ((time.time() - start_time)/60*66/hits)
            print ">>> Avg time loops: %.1f sec, Avg time upload: %.1f sec, Avg time total: %.1f sec (target 12)" % (tot_loops/(found_optimal+found_suboptimal), tot_upload/(found_optimal+found_suboptimal), (time.time() - start_time)/(found_optimal+found_suboptimal))
        if found_optimal > 0 and found_suboptimal > 0:
            print ">>> Loop stats: optimal %d (avg %.1f), suboptimal %d (avg %.1f)" % (found_optimal, float(found_optimal_loops)/found_optimal, found_suboptimal, float(found_suboptimal_loops)/found_suboptimal)

    if 'hands' in l:
        hands = json.loads(l.partition("=")[2])
        print ">>> hands = %s" % hands

        start_loops = time.time()
        
        opts = {}
        for hand in hands:
            opts[hand] = {}
        loops = 0
        # Make options
        while True:
            loops += 1
            threads = {}
            # For each hand make some new options
            for hand in hands:
                threads[hand] = pool.apply_async(make_options, (hand,))
            for hand in hands:
                opts[hand].update(threads[hand].get())
                print ">>> hand %s (%d options)" % (hand, len(opts[hand]))

            choice01 = set(opts[hands[0]].keys()) & set(opts[hands[1]].keys())
            choice12 = set(opts[hands[1]].keys()) & set(opts[hands[2]].keys())
            choice02 = set(opts[hands[0]].keys()) & set(opts[hands[2]].keys())
            choice012 = choice01 & choice12
            
            if ALLOW_SUBOPTIMAL:
                choice = choice01 | choice02 | choice12
            else:
                choice = choice012
                
            if choice:
                break
            print ">>> Need more options..."

        print ">>> Choices:", choice

        if choice012:   # All three match, 100% chance
            choice = list(choice012)[0]
            found_optimal += 1
            found_optimal_loops += loops
        else:  # Any double, 50% chance
            choice = list(choice)[0]
            found_suboptimal += 1
            found_suboptimal_loops += loops
        
        tot_loops += time.time() - start_loops

    if 'how many' in l:
        if choice is None:
            print ">>> Skipping..."
            s.send("1\n")
        else:
            print ">>> Sending %d" % choice[1]
            s.send("%d\n" % choice[1])

    if 'the magic' in l:
        if choice is None:
            print ">>> Skipping..."
            s.send("\n")
        else:
            print ">>> Sending %d" % int(choice[0],16)
            s.send("%d\n" % int(choice[0],16))

    if 'here is mine' in l:
        bosschoice = l.partition(': ')[2]
        print ">>> Boss choice %s" % bosschoice
        ourchoice = hands[ (hands.index(bosschoice)+1)%3 ]
        print ">>> Our optimal choice %s" % ourchoice
        if choice in opts[ourchoice]:  # Yes!
            pass
        else:
            print ">>> Optimal not available, go for draw"
            ourchoice = bosschoice
            choice = None

    if 'show me the secret' in l:
        if choice is None:
            print ">>> Skipping..."
            draws += 1
            s.send("\n")
        else:
            start_upload = time.time()
            print ">>> Sending data..."
            data = "".join(x[0] for x in opts[ourchoice][choice]) + "\n"
            print ">>>    %s..." % data[:50],
            while data:
                print " %d " % len(data),
                try:
                    sent = s.send(data)
                except socket.timeout:
                    continue
                data = data[sent:]
            print "done"

    if 'Boss is going home' in l:
        sys.exit(1)

    if 'boss hp -=' in l:
        tot_upload += time.time() - start_upload
        hits += 1
    if 'nothing happened' in l:
        tot_upload += time.time() - start_upload
        draws += 1
