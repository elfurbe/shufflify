#!/usr/bin/python

import sys,getopt

def usage():
    print "usage: ",sys.argv[0]," [-hl] -m METHOD -i FILENAME [-o FILENAME]"
    print "-h, --help               show this help"
    print "-l, --list               list available shuffle methods"
    print "-m, --method=METHOD      shuffling method"
    print "-i, --infile=FILE        input file of spotify URLs"
    print "-o, --outfile=FILE       output to specified file instead of stdout"

def parse_plugins(plugindir):
    print "Plugin directory:",plugindir
    print "This will parse the plugins and build the plugin list"

def list_plugins():
    parse_plugins("plugins")
    print "This will be a list of plugins"

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hlm:i:o:",["help","list","method=","infile=","outfile="])
    except getopt.GetoptError:
        print "Options not recognized."
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
            list_plugins()
            sys.exit(0)
        elif opt in ("-m","--method"):
            method = arg
        elif opt in ("-i","--infile"):
            infile = arg
        elif opt in ("-o","--outfile"):
            outfile = arg
    if not method or not infile:
        print "Must specify a method and an input file"
        usage()
        sys.exit(2)

    print 'Method:', method
    print 'Input file:', infile
    
    if outfile:
        print 'Output file:', outfile

if __name__ == "__main__":
    main(sys.argv[1:])
