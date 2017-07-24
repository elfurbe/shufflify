#!/usr/bin/env python

import sys
import getopt
import os
import collections
import abc
import imp
import random
import json
import subprocess
import progressbar
from pprint import pprint

class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    description = "string"

    @abc.abstractmethod
    def shuffle(self,artists):
        """Do yo' shufflin' bidness and return the array of tracks"""
        tracklist = ""
        return tracklist


def usage():
    print "usage: ",sys.argv[0]," [-hl] -p PLUGIN -i FILENAME [-o FILENAME]"
    print "-h, --help               show this help"
    print "-l, --list               list available shuffle plugins"
    print "-p, --plugin=PLUGIN      shuffling plugin, default is furbinate"
    print "-i, --infile=FILE        input file of spotify URLs"
    print "-o, --outfile=FILE       output to specified file instead of stdout"
    print "-u, --url=PLAYLISTURL    public playlist url"

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
    #plugins = ['furbify','qwijify','ogr','lcm','balanced']
    #print "Plugin directory:",plugindir
    #print "This will parse the plugins and build the plugin list"
    return plugins

def list_plugins(plugins):
    #print "This will be a list of plugins"
    for plugin in plugins:
        imp.load_source("shuffler","plugins/"+plugin+".py")
        from shuffler import shuffler
        active = shuffler()
        print (plugin+":\t"+active.description).expandtabs(15)
        active = None

def main(argv):
    plugin_dir = "plugins"
    plugins = parse_plugins(plugin_dir)

    try:
        opts, args = getopt.getopt(argv,"hlp:i:o:u:",["help","list","plugin=","infile=","outfile=","url="])
    except getopt.GetoptError, exc:
        print exc.msg
        usage()
        sys.exit(2)

    plugin = ''
    infile = ''
    outfile = ''
    url = ''
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

    if not infile and not url:
        print "Must specify input file or playlist url"
        usage()
        sys.exit(2)

    if not plugin:
        plugin = "furbinate"

    print 'Plugin:', plugin
    if infile:
        print 'Input file:', infile
    elif url:
        print 'Input url:', url
    
    if outfile:
        print 'Output file:', outfile

    #plugin = __import__(plugin)
    imp.load_source("shuffler","plugins/"+plugin+".py")
    from shuffler import shuffler
    active = shuffler()
    #print active.description

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
            try:
                rawjson = subprocess.check_output("curl -s "+url+" 2>&1| grep Spotify.Entity | sed -e 's/^[ \t]*Spotify.Entity\ =\ //' -e 's/;$//g'",shell=True)
                parsed = json.loads(rawjson)
                count += 1
            except ValueError:
                print "Parse failed for: "+url
                count += 1
                continue
            artist = parsed['artists'][0]['name'] 
            artist = artist.replace(",","")
            #print artist, url
            artists[artist].append(url)
            bar.update(count)

        bar.finish()
    elif url:
        rawjson = subprocess.check_output("curl -s "+url+" 2>&1| grep Spotify.Entity | sed -e 's/^.*Spotify.Entity\ =\ //g' -e 's/;$//g'",shell=True)
        parsed = json.loads(rawjson)
        if parsed["tracks"]["total"] > parsed["tracks"]["limit"]:
            print "Playlists with more than "+str(parsed["tracks"]["limit"])+" tracks do not work by url."
            sys.exit(3)
        for item in parsed["tracks"]["items"]:
            artist = item['track']['artists'][0]['name']
            artist = artist.replace(",","")
            trackurl = item['track']['external_urls']['spotify']
            #print artist, trackurl
            artists[artist].append(trackurl)

    if len(artists) <= 1:
        print "There's only one artist, you fuckin' maroon.\n*WAVES HANDS* THERE! It's shuffled, dick."
        for artist,tracks in artists.iteritems():
            for track in tracks:
                print track
        sys.exit()
    
    columns = active.shuffle(artists)
    for column in columns:
        for tracks in column:
            explode = tracks.split(",")
            print explode[1]

if __name__ == "__main__":
    main(sys.argv[1:])
