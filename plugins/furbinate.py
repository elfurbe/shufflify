from shufflify import PluginBase
import random

class shuffler(PluginBase):

    description = "The original. Still the best. The rest of this is fucking snake oil. (old)"
    
    def shuffle(self,artists):
        max_len = 0
        for artist,tracks in artists.items():
            print(artist+": "+str(len(tracks)))
            if len(tracks) > max_len:
                max_len = len(tracks)

        for artist,tracks in artists.items():
            if len(tracks) < max_len:
                dummies = max_len - len(tracks)
                dummy_positions = random.sample(range(0,max_len),dummies)
                random.shuffle(tracks)
                for dummy in dummy_positions:
                    tracks.insert(dummy,0)
            else:
                continue

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
                shuffles = 0
                colnumtracks = len(column)
                if (colnumtracks == 1) and (last_column[-1].split(",")[0] == column[0].split(",")[0]):
                    print("Welp, we fucked. "+column[0].split(",")[0]+" is the only artist in this column.")
                else:
                    while (last_column[-1].split(",")[0] == column[0].split(",")[0]) and (shuffles < 10):
                        print("Artist match for "+column[0].split(",")[0]+". Shufflin': "+str(shuffles))
                        random.shuffle(column)
                        shuffles += 1
            columns.append(column)
        return columns
