#!/usr/bin/env python

import sys,getopt,os
import collections
from pprint import pprint

def usage():
    print "usage: ",sys.argv[0]," [-hl] -p PLUGIN -i FILENAME [-o FILENAME]"
    print "-h, --help               show this help"
    print "-l, --list               list available shuffle plugins"
    print "-p, --plugin=PLUGIN      shuffling plugin"
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

    file = open(path+'__init__.py','w')

    toWrite = '__all__ = '+str(imps)

    file.write(toWrite)
    file.close()
    return imps

def parse_plugins(plugindir):
    plugins = loadImports('plugins/')
    from plugins import *
    #plugins = ['furbify','qwijify','ogr','lcm','balanced']
    #print "Plugin directory:",plugindir
    #print "This will parse the plugins and build the plugin list"
    return plugins

def list_plugins(plugins):
    #print "This will be a list of plugins"
    pprint(plugins)

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

    if not plugin or not infile:
        print "Must include plugin and input file at minimum"
        usage()
        sys.exit(2)

    print 'Plugin:', plugin
    print 'Input file:', infile
    
    if outfile:
        print 'Output file:', outfile

if __name__ == "__main__":
    main(sys.argv[1:])
