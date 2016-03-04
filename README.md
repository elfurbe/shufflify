# shufflify
All shuffle sucks, Spotify's included. This is a series of experiments employing different methods of shuffling a list of spotify URLs to attempt to ensure two things:<br />
1. You never hear two songs by the same artist back-to-back
2. You never end up with a repeating pattern of artists

shufflify.py - the simplest option. Uses a series of random shuffles and dummy inserts to create variance. Actually works pretty well, but it's just TOO EASY. This is actually the only one that works, so far.

shufflify-balanced.py - This shuffles using an approximate implementation of Martin Fiedler's algorithm described here: http://keyj.emphy.de/balanced-shuffle/. The implementation is currently not complete. 

lcmshuffle.py - Uses the lowest common multiple to create an evenly divisible space within which each artist's tracks are distributed randomly within even segments of the total length. Unfortunately, due to the large space size, the introduction of back-to-back artists in the final list is very likely and difficult to fix.

ogrshuffle.py - Uses an optimal golomb ruler to space artist tracks in a guaranteed non-uniform way across the smallest space that satisfies that mathematical constraint. Due to the non-linear increase in length with track count, creates stacks of the most prolific artist somewhere within the distribution depending on padding method.
