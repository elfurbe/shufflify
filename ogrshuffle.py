#!/usr/bin/env python
from lxml import html
import requests
import random
import sys
import collections
from ogr100 import ogr

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

for artist,tracks in artists.iteritems():
    random.shuffle(tracks)
    length = len(tracks) - 1
    new_tracks = []
    if length != 0:
        for spaces in ogr(length):
            new_tracks.append(tracks.pop())
            new_tracks.extend([0] * spaces)
    new_tracks.append(tracks.pop())
    artists[artist] = new_tracks

#artists_order = sorted(artists, key=lambda k: len(artists[k]), reverse=True)

max_len = 0
#for i in xrange(len(artists_order)):
#    artist = artists_order[i]
#    tracks = artists[artist]
#    tracks.reverse()
#    tracks.extend([0] * i)
#    tracks.reverse()
#    if len(tracks) > max_len:
#        max_len = len(tracks)

for artist,tracks in artists.iteritems():
    if len(tracks) > max_len:
        max_len = len(tracks)

for artist,tracks in artists.iteritems():
    if len(tracks) < max_len:
        pad = max_len - len(tracks)
        if pad % 2 == 0:
            halfsies = pad / 2
        else:
            pad += 1
            halfsies = pad / 2
        tracks.extend([0] * halfsies)
        tracks.reverse()
        tracks.extend([0] * halfsies)
        tracks.reverse()

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
