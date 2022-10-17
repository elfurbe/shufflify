#!/usr/bin/env python3

import sys
import getopt
import os
import collections
import abc
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
    #plugins = ['furbify','qwijify','ogr','lcm','balanced']
    #print("Plugin directory:",plugindir)
    #print("This will parse the plugins and build the plugin list")
    return plugins

def load_module_from_file(module_name, module_path):
    """Loads a python module from the path of the corresponding file.
    Args:
        module_name (str): namespace where the python module will be loaded,
            e.g. ``foo.bar``
        module_path (str): path of the python file containing the module
    Returns:
        A valid module object
    Raises:
        ImportError: when the module can't be loaded
        FileNotFoundError: when module_path doesn't exist
    """
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    elif sys.version_info[0] == 3 and sys.version_info[1] < 5:
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader(module_name, module_path)
        module = loader.load_module()
    elif sys.version_info[0] == 2:
        import imp
        module = imp.load_source(module_name, module_path)
    return module

def list_plugins(plugins):
    #print("This will be a list of plugins")
    for plugin in plugins:
        module = load_module_from_file(shuffle_plugin,"plugins/"+plugin+".py")
        sys.modules[shuffler] = module
        from shuffler import shuffler
        active = shuffler()
        print(plugin+":\t"+active.description).expandtabs(15)
        active = None

def main(argv):
    plugin_dir = "plugins"
    plugins = parse_plugins(plugin_dir)

    try:
        opts, args = getopt.getopt(argv,"hlep:i:o:u:",["help","list","export","plugin=","infile=","outfile=","url="])
    except getopt.GetoptError as err:
        print(err)
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
        plugin = "furbinate"

    print('Plugin:', plugin)
    if infile:
        print('Input file:', infile)
    elif url:
        print('Input url:', url)
    
    if outfile:
        print('Output file:', outfile)

    #plugin = __import__(plugin)
    module = load_module_from_file("shuffler","plugins/"+plugin+".py")
    sys.modules["shuffler"] = module
    from shuffler import shuffler
    active = shuffler()
    #print(active.description)

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
                print("Parse failed for: "+url)
                count += 1
                continue
            #print(json.dumps(parsed, indent=2))
            artist = parsed['artists'][0]['name'] 
            album = parsed['album']['name']
            track = parsed['name']
            if export:
                print(track+" - "+artist+" - "+album)
                continue
            artist = artist.replace(",","")
            #print(artist, url)
            artists[artist].append(url)
            bar.update(count)

        #sys.exit(1)
        bar.finish()
    elif url:
        rawjson = subprocess.check_output("curl -s "+url+" 2>&1| grep Spotify.Entity | sed -e 's/^.*Spotify.Entity\ =\ //g' -e 's/;$//g'",shell=True)
        parsed = json.loads(rawjson)
        #print(json.dumps(parsed, indent=2))
        #sys.exit(1)
        if parsed["tracks"]["total"] > parsed["tracks"]["limit"]:
            print("Playlists with more than "+str(parsed["tracks"]["limit"])+" tracks do not work by url.")
            sys.exit(3)
        for item in parsed['tracks']['items']:
            #print(json.dumps(item, indent=4))
            #sys.exit(1)
            if not item['is_local']:
                artist = item['track']['artists'][0]['name']
                album = item['track']['album']['name']
                track = item['track']['name']
                if export:
                    print(track+" - "+artist+" - "+album)
                    continue
                artist = artist.replace(",","")
                trackurl = item['track']['external_urls']['spotify']
                #print(artist, trackurl)
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
    for column in columns:
        for tracks in column:
            explode = tracks.split(",")
            print(explode[1])

if __name__ == "__main__":
    main(sys.argv[1:])
