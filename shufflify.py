#!/usr/bin/env python

import sys,getopt,os
import collections
from pprint import pprint

def usage():
    print "usage: ",sys.argv[0]," [-hl] -m METHOD -i FILENAME [-o FILENAME]"
    print "-h, --help               show this help"
    print "-l, --list               list available shuffle methods"
    print "-m, --method=METHOD      shuffling method"
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

def parse_plugins(plugindir):
    loadImports('plugins/')
    #from plugins import *
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
        opts, args = getopt.getopt(argv,"hlm:i:o:",["help","list","method=","infile=","outfile="])
    except getopt.GetoptError, exc:
        print exc.msg
        usage()
        sys.exit(2)

    method = ''
    infile = ''
    outfile = ''
    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit(0)
        elif opt in ("-l","--list"):
            list_plugins(plugins)
            sys.exit(0)
        elif opt in ("-m","--method"):
            method = arg
        elif opt in ("-i","--infile"):
            infile = arg
        elif opt in ("-o","--outfile"):
            outfile = arg

    if not method or not infile:
        print "Must include method and input file at minimum"
        usage()
        sys.exit(2)

    print 'Method:', method
    print 'Input file:', infile
    
    if outfile:
        print 'Output file:', outfile

if __name__ == "__main__":
    main(sys.argv[1:])
