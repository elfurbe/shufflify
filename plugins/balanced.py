import abc
from shufflify import PluginBase
import random

class shuffler(PluginBase):

    description = "An attempt to implement Martin Fielder's algorithm (does not work)"
    
    def shuffle(self,artists):
        max_len = 0
        for artist,tracks in artists.items():
            print(artist+": "+str(len(tracks)))
            if len(tracks) > max_len:
                max_len = len(tracks)

        for artist,tracks in artists.items():
            random.shuffle(tracks)
            trackcount = len(tracks)
            if trackcount < max_len:
                dummies = max_len - trackcount
                n = max_len
                new_order = []

                while n > 0:
                    if trackcount > dummies:
                        k = n / trackcount
                        r = n / k
                        noise = random.randint(0,10)
                        coinflip = random.randint(0,1)
                        if coinflip == 0:
                            r = round(r + (k * noise / 100))
                        else:
                            r = round(r - (k * noise / 100)) 
                        new_order.append(0)
                        start = max_len - n
                        for i in range(start,start+r-2):
                            new_order.append(tracks.pop())
                    elif dummies > trackcount:
                        k = n / dummies
                        r = n / k
                        noise = random.randint(0,10)
                        coinflip = random.randint(0,1)
                        if coinflip == 0:
                            r = round(r + (k * noise / 100))
                        else:
                            r = round(r - (k * noise / 100)) 
                        new_order.append(tracks.pop())
                        for i in range(0,r-2):
                            new_order.append(0)
                    else:
                        continue
                    n = n - r
                tracks = new_order           
                    
        columns = []
        for i in range(max_len):
            column = []
            for artist,tracks in artists.items():
                if tracks[i] != 0:
                    entry = artist + "," + tracks[i]
                    column.append(entry)
            random.shuffle(column)
            if i > 0:
                last_column = columns[-1]
                while last_column[-1].split(",")[0] == column[0].split(",")[0]:
                    random.shuffle(column)
            columns.append(column)

        tracklist_ordered = []
        for column in columns:
            for track in column:
                explode = track.split(",")
                tracklist_ordered.append(explode[1])

        return tracklist_ordered
