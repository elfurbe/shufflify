#!/usr/bin/env python

import sys
import getopt
import os
import collections
import abc
import imp
import random
import requests
from pprint import pprint
from lxml import html

class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    description = "string"

    @abc.abstractmethod
    def describe(self):
        """Print out your description when I tells you"""
        return self.descritpion

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
        opts, args = getopt.getopt(argv,"hlp:i:o:",["help","list","plugin=","infile=","outfile="])
    except getopt.GetoptError, exc:
        print exc.msg
        usage()
        sys.exit(2)

    plugin = ''
    infile = ''
    outfile = ''
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

    if not infile:
        print "Must specify input file"
        usage()
        sys.exit(2)

    if not plugin:
        plugin = "furbinate"

    print 'Plugin:', plugin
    print 'Input file:', infile
    
    if outfile:
        print 'Output file:', outfile

    #plugin = __import__(plugin)
    imp.load_source("shuffler","plugins/"+plugin+".py")
    from shuffler import shuffler
    active = shuffler()
    #print active.description

    with open(infile, 'r') as infile:
        data = infile.read()

    urls = data.splitlines()
    random.shuffle(urls)

    artists = collections.defaultdict(list)

    for url in urls:
        page = requests.get(url)
        tree = html.fromstring(page.content)

        artist = tree.xpath('//span[@class="creator-name"]/text()')[0]
        artist = artist.replace(",","")
        #print artist, url
        artists[artist].append(url)

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
