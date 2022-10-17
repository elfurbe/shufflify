#!/usr/bin/env python3

import sys
import getopt
import os
import collections
import abc
from importlib.machinery import SourceFileLoader
import random
import json
import subprocess
import progressbar
from pprint import pprint
import configparser
import asyncio
from spotipy2 import Spotify
from spotipy2.auth import ClientCredentialsFlow
import argparse

class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    description = "string"

    @abc.abstractmethod
    def shuffle(self,artists):
        """Do yo' shufflin' bidness and return the array of tracks"""
        tracklist = ""
        return tracklist

def loadImports(path):
    files = os.listdir(path)
    imps = []

    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
               name = name[0]
               imps.append(name)
    return imps

def parse_plugins(plugindir):
    plugins = loadImports('plugins/')
    return plugins

def list_plugins(plugins):
    print("Available plugins:\n")
    for plugin in plugins:
        SourceFileLoader("shuffler","plugins/"+plugin+".py").load_module()
        from shuffler import shuffler
        active = shuffler()
        print(f"{plugin}:\t{active.description}".expandtabs(15))
        active = None

async def get_track(url):
    client = Spotify(
        ClientCredentialsFlow(
            client_id = config['spotify']['client_id'],
            client_secret = config['spotify']['client_secret']
        )
    )

    track_id = str(url.rsplit('/', 1)[-1])
    async with client as s:
        track = await s.get_track(track_id)
        return track

async def get_playlist_metadata(url):
    client = Spotify(
        ClientCredentialsFlow(
            client_id = config['spotify']['client_id'],
            client_secret = config['spotify']['client_secret']
        )
    )

    playlist_id = str(url.rsplit('/', 1)[-1].rsplit('?', 1)[0])
    async with client as s:
        playlist = await s.get_playlist(playlist_id)
        return playlist



async def get_playlist_tracks(playlist_id):
    client = Spotify(
        ClientCredentialsFlow(
            client_id = config['spotify']['client_id'],
            client_secret = config['spotify']['client_secret']
        )
    )

    async with client as s:
        async for track in s.iter_playlist_tracks(playlist_id):
            yield track

async def process_playlist(playlist_id):
    tracks = []
    async for item in get_playlist_tracks(playlist_id):
        tracks.append(item.track)

    return tracks

def main(argv):
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

    plugin_dir = "plugins"
    plugins = parse_plugins(plugin_dir)

    parser = argparse.ArgumentParser(description="Shufflify: All Shuffle Sucks, Guess We'll Do It Ourselves")
    parser.add_argument("-p","--plugin", type=str, default="furbinate2", help="Choose specific plugin, default: furbinate2")
    parser.add_argument("-e","--export", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l","--list", action="store_true", help="List available plugins")
    group.add_argument("-i","--infile", type=str)
    group.add_argument("-u","--url", type=str)

    args = parser.parse_args()

    if args.list:
        list_plugins(plugins)
        sys.exit(0)

    plugin = args.plugin
    print('Plugin:', plugin)
    
    SourceFileLoader("shuffler","plugins/"+plugin+".py").load_module()
    from shuffler import shuffler
    active = shuffler()

    artists = collections.defaultdict(list)
    if args.infile:
        print(f"input file: {args.infile}\n")
        with open(args.infile, 'r') as infile:
            data = infile.read()

        urls = data.splitlines()
        random.shuffle(urls)
        count = 0
        total = len(urls)

        bar = progressbar.ProgressBar(redirect_stdout=True)
        for url in bar(urls):
            if url.startswith('https://open.spotify.com/local'):
                continue
            track_obj = asyncio.run(get_track(url))
            track = str(track_obj.name)
            album = str(track_obj.album)
            artist = str(track_obj.artists[0].name)
            if args.export:
                print(track+" - "+artist+" - "+album)
                continue
            artist = artist.replace(",","")
            artists[artist].append(url)

    elif args.url:
        print(f"Input url: {args.url}")
        print("")
        playlist = asyncio.run(get_playlist_metadata(args.url))
        print(f"Playlist: {playlist.name}")
        print(f"Playlist ID: {playlist.id}")
        tracks = asyncio.run(process_playlist(playlist.id))
        print(f"Track Count: {len(tracks)}")
        print("")
        for track_obj in tracks:
            if not track_obj.is_local:
                track = str(track_obj.name)
                artist = str(track_obj.artists[0].name)
                album = str(track_obj.album)
                trackurl = str(track_obj.external_urls['spotify'])
                if args.export:
                    print(track+" - "+artist+" - "+album)
                    continue
                artist = artist.replace(",","")
                artists[artist].append(trackurl)

    if args.export:
        print("")
        print("A list of tracks as text formatted like above is what Jason wanted, so that's what it does and has done.")
        print("And now, I die.")
        sys.exit(0)

    if len(artists) <= 1:
        print("There's only one artist, you fuckin' maroon.\n*WAVES HANDS* THERE! It's shuffled, dick.")
        for artist,tracks in artists.items():
            for track in tracks:
                print(track)
        sys.exit()
    
    columns = active.shuffle(artists)
    print("")
    for column in columns:
        for tracks in column:
            explode = tracks.split(",")
            print(explode[1])

if __name__ == "__main__":
    main(sys.argv[1:])
