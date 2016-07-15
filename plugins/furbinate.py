from shufflify import PluginBase
import random

class shuffler(PluginBase):

    description = "The original. Still the best. The rest of this is fucking snake oil."
    
    def shuffle(self,artists):
        max_len = 0
        for artist,tracks in artists.iteritems():
            if len(tracks) > max_len:
                max_len = len(tracks)

        for artist,tracks in artists.iteritems():
            if len(tracks) < max_len:
                dummies = max_len - len(tracks)
                dummy_positions = random.sample(xrange(max_len),dummies)
                random.shuffle(tracks)
                for dummy in dummy_positions:
                    tracks.insert(dummy,0)
            else:
                continue

        columns = []
        for i in range(max_len):
            column = []
            for artist,tracks in artists.iteritems():
                if tracks[i] != 0:
                    entry = artist + "," + tracks[i]
                    column.append(entry)
            random.shuffle(column)
            if i > 0:
                last_column = columns[-1]
                while last_column[-1].split(",")[0] == column[0].split(",")[0]:
                    random.shuffle(column)
            columns.append(column)
        return columns
