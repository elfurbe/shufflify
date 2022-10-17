# shufflify
All shuffle sucks, Spotify's included. This is a series of experiments employing different methods of shuffling a playlist and/or list of spotify track URLs to attempt to ensure two things:<br />
1. You never hear two songs by the same artist back-to-back<br />
2. You never end up with a repeating pattern of artists<br />

Updated for python3, nothing works in python2 any more, I don't care, you don't care, get with the times, square.

Thanks to Spofify taking all the convenient JSON objects out of their html pages, I had to pivot to the actual API like some kind of monster. It's worse in most ways, it requires developer app credentials from Spotify, but here we are. I'm not leaving my creds in here for you animals, but you can get yourself credentials by making a new app here: https://developer.spotify.com/dashboard/applications Put the client_id and client_secret in `config.ini` and things should do what needs done. I left `shufflify.py` where it is for historical confusion but you'll want to use `shufflify2.py` now.

Dependencies:
 - python3
 - progressbar2 (https://github.com/WoLpH/python-progressbar, pip install progressbar2)
 - spotipy2

Because we're neck deep in API calls now, the easiest way to bring data in for shufflin' is to get yourself a playlist url. You can get that from the playlist view in the Spotify client, three dots, share, copy playlist url, just pass that to shufflify with the `-u` option, probably put it in quotes cause shells are the devil, and it will spit out a long list of urls. Copy those to your clipboard, open a clean new playlist in Spotify and just paste in there and it'll populate with tracks. I hear you asking "why can't I just sign in with my spotify account and let the tool make a new playlist" and no, I will not do that, I do not care, final answer.

The Plugins:
 - furbinate2 - the simplest option. Uses a series of random shuffles and dummy inserts to create variance. Actually works pretty well, but it's just TOO EASY. This is actually the only one that works, so far.
 - balanced - This shuffles using an approximate implementation of Martin Fiedler's algorithm described here: http://keyj.emphy.de/balanced-shuffle/. The implementation is currently not complete.
 - lcm - Uses the lowest common multiple to create an evenly divisible space within which each artist's tracks are distributed randomly within even segments of the total length. Unfortunately, due to the large space size, the introduction of back-to-back artists in the final list is very likely and difficult to fix.
 - ogr - Uses an optimal golomb ruler to space artist tracks in a guaranteed non-uniform way across the smallest space that satisfies that mathematical constraint. Due to the non-linear increase in length with track count, creates stacks of the most prolific artist somewhere within the distribution depending on padding method.
 - qwijify - Some random BS Jason told me would work that didn't but I wrote it anyway and now his shame will be imortalized for all time
