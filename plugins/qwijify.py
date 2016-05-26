#!/usr/bin/env python
import random
import collections
import math

DEBUG = False

def debug(m):
    if DEBUG:
        print m

num_tracks = 11
tracklist = []
for _ in range(num_tracks):
   tracklist.append(1)

max_len = 20
tracklist_len = len(tracklist)

num_spaces = max_len - tracklist_len

spaces_per = num_spaces / (tracklist_len * 1.0)

debug("Initial tracklist len: " + str(tracklist_len))
debug("Max len: "+str(max_len))
debug("Initial num_spaces: "+str(num_spaces))
debug("Initial spaces_per: "+str(spaces_per))

padded_tracklist = []
while len(tracklist) > 0:
    debug("Tracks left: "+str(len(tracklist)))
    padded_tracklist.append(tracklist.pop())
    spaces_per = num_spaces / (tracklist_len * 1.0)
    debug("spaces_per: "+str(spaces_per))
    coinflip = random.randint(0,1)
    debug("Coinflip: "+str(coinflip))
    if coinflip == 0:
        spaces = int(math.floor(spaces_per))
        debug("Spaces: "+str(spaces))
        for _ in range(spaces):
            padded_tracklist.append(0)
        num_spaces = num_spaces - spaces
    else:
        spaces = int(math.ceil(spaces_per))
        debug("Spaces: "+str(spaces))
        for _ in range(spaces):
            padded_tracklist.append(0)
        num_spaces = num_spaces - spaces

if len(padded_tracklist) < max_len:
    for _ in range(max_len - len(padded_tracklist)):
        padded_tracklist.append(0)
print "Jason:\t\t",padded_tracklist

tracklist = []
for _ in range(num_tracks):
   tracklist.append(1)

dummies = max_len - len(tracklist)
dummy_positions = random.sample(xrange(max_len),dummies)
random.shuffle(tracklist)
for dummy in dummy_positions:
    tracklist.insert(dummy,0) 

print "random.sample:\t",tracklist

tracklist = []
for _ in range(num_tracks):
   tracklist.append(1)

trackcount = len(tracklist)
dummies = max_len - trackcount
n = max_len
new_order = []

while n > 0:
    debug("loop start n: "+str(n))
    trackcount = len(tracklist)
    if trackcount > dummies:
        debug("trackcount is greater")
        k = n / (trackcount * 1.0)
        debug("k: "+str(k))
        r = n / (k * 1.0)
        debug("r: "+str(r))
        noise = random.randint(0,10)
        debug("noise: "+str(noise))
        coinflip = random.randint(0,1)
        debug("coinflip: "+str(coinflip))
        if coinflip == 0:
            r = round(r + (k * (noise / (100 * 1.0))))
        else:
            r = round(r - (k * (noise / (100 * 1.0))))
        debug("randomized r: "+str(r))
        new_order.append(0)
        dummies = dummies - 1 
        debug("dummies: "+str(dummies))
        start = max_len - n
        debug("range: "+str(start+r-2))
        for _ in range(int(start+r-2)):
            debug("for loop: "+str(_)+str(tracklist))
            new_order.append(tracklist.pop())
    elif dummies > trackcount:
        debug("dummies is greater")
        k = n / dummies
        debug("k: "+str(k))
        r = n / k
        debug("r: "+str(r))
        noise = random.randint(0,10)
        debug("noise: "+str(noise))
        coinflip = random.randint(0,1)
        debug("coinflip: "+str(coinflip))
        if coinflip == 0:
            r = round(r + (k * noise / 100))
        else:
            r = round(r - (k * noise / 100))
        debug("randomized r: "+str(r))
        new_order.append(tracklist.pop())
        start = dummies - n
        debug("range: "+str(start+r-2))
        for _ in range(int(start+r-2)):
            new_order.append(0)
            dummies = dummies - 1
    else:
        continue
    n = n - r
    debug("loop end n: "+str(n))
    debug("loop end tracklist: "+str(new_order))
offset = random.randint(1,max_len)
debug("offset: "+str(offset))
for _ in range(offset):
    new_order.append(new_order.pop(0))

print "balanced:\t",new_order
