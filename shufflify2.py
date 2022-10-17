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

class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    description = "string"

    @abc.abstractmethod
    def shuffle(self,artists):
        """Do yo' shufflin' bidness and return the array of tracks"""
        tracklist = ""
        return tracklist

def usage():
    print("usage: ",sys.argv[0]," [-hl] -p PLUGIN -i FILENAME [-o FILENAME]")
    print("-h, --help               show this help")
    print("-l, --list               list available shuffle plugins")
    print("-e, --export             print track metadata as export-friendly text and exit")
    print("-p, --plugin=PLUGIN      shuffling plugin, default is furbinate")
    print("-i, --infile=FILE        input file of spotify URLs")
    print("-o, --outfile=FILE       output to specified file instead of stdout")
    print("-u, --url=PLAYLISTURL    public playlist url")

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
    for plugin in plugins:
        imp.load_source("shuffler","plugins/"+plugin+".py")
        from shuffler import shuffler
        active = shuffler()
        print(plugin+":\t"+active.description).expandtabs(15)
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

    try:
        opts, args = getopt.getopt(argv,"hlep:i:o:u:",["help","list","export","plugin=","infile=","outfile=","url="])
    except getopt.GetoptError(exc):
        print(exc.msg)
        usage()
        sys.exit(2)

    plugin = ''
    infile = ''
    outfile = ''
    url = ''
    export = False
    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit(0)
        elif opt in ("-l","--list"):
            list_plugins(plugins)
            sys.exit(0)
        elif opt in ("-p","--plugin"):
            plugin = arg
        elif opt in ("-i","--infile"):
            infile = arg
        elif opt in ("-o","--outfile"):
            outfile = arg
        elif opt in ("-u","--url"):
            url = arg
        elif opt in ("-e","--export"):
            export = True

    if not infile and not url:
        print("Must specify input file or playlist url")
        usage()
        sys.exit(2)

    if not plugin:
        plugin = "furbinate2"

    print('Plugin:', plugin)
    if infile:
        print('Input file:', infile)
    elif url:
        print('Input url:', url)
        print("")
    
    if outfile:
        print('Output file:', outfile)

    #plugin = __import__(plugin)
    #imp.load_source("shuffler","plugins/"+plugin+".py")
    SourceFileLoader("shuffler","plugins/"+plugin+".py").load_module()
    from shuffler import shuffler
    active = shuffler()

    artists = collections.defaultdict(list)
    if infile:
        with open(infile, 'r') as infile:
            data = infile.read()

        urls = data.splitlines()
        random.shuffle(urls)
        count = 0
        total = len(urls)

        bar = progressbar.ProgressBar(redirect_stdout=True,max_value=total)
        for url in urls:
            count += 1
            track_obj = asyncio.run(get_track(url))
            track = str(track_obj.name)
            album = str(track_obj.album)
            artist = str(track_obj.artists[0].name)
            if export:
                print(track+" - "+artist+" - "+album)
                continue
            artist = artist.replace(",","")
            artists[artist].append(url)
            bar.update(count)

        #sys.exit(1)
        bar.finish()

    elif url:
        playlist = asyncio.run(get_playlist_metadata(url))
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
                if export:
                    print(track+" - "+artist+" - "+album)
                    continue
                artist = artist.replace(",","")
                artists[artist].append(trackurl)

    if export:
        sys.exit()

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
