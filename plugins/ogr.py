import abc
from shufflify import PluginBase

class shuffler(PluginBase):

    description = "Uses an optimal golomb ruler to space artist tracks in a non-uniform way"
    
    def describe(self):
        return self.description

    def shuffle(artists):
        return
