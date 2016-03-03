#!/usr/bin/env python
from lxml import html
import requests
import random
import sys
import collections

def gcd(a, b):
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmm(args):
    return reduce(lcm, args)


urllist = sys.argv[1]
with open(urllist, 'r') as infile:
        data = infile.read()

urls = data.splitlines()
random.shuffle(urls)

artists = collections.defaultdict(list)

for url in urls:
    page = requests.get(url)
    tree = html.fromstring(page.content)

    artist = tree.xpath('//span[@class="artist-name"]/text()')[0]
    artists[artist].append(url)

tracklens = []
for artist,tracks in artists.iteritems():
    tracklens.append(len(tracks))


max_len = lcmm(tracklens)

artists_with_pad = collections.defaultdict(list)
for artist,tracks in artists.iteritems():
    random.shuffle(tracks)
    tracks_length = len(tracks)
    seg_length = max_len / tracks_length
    tracks_padded = []
    for track in tracks:
        seg = [0] * seg_length
        track_pos = random.sample(xrange(seg_length),1)[0]
        seg[track_pos] = track
        tracks_padded = tracks_padded + seg
    artists_with_pad[artist] = tracks_padded

artists = artists_with_pad

columns = []
for i in xrange(max_len):
    column = []
    for artist,tracks in artists.iteritems():
        if tracks[i] != 0:
            entry = artist + "," + tracks[i]
            column.append(entry)
    if len(column) == 0:
        continue
    random.shuffle(column)
    if i > 0 and len(columns) > 0:
        last_column = columns[-1]
        if len(last_column) > 0 and len(column) > 0:
            if last_column[-1].split(",")[0] == column[0].split(",")[0]:
                first = column[0]
                last = column[-1]
                column[0] = last
                column[-1] = first
    columns.append(column)
    
for column in columns:
    for tracks in column:
        explode = tracks.split(",")
        print explode[1]
