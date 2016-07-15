import abc
from shufflify import PluginBase

class shuffler(PluginBase):

    description = "Uses lowest-common-multiple to create even distributions"
    
    def describe(self):
        return self.description

    def shuffle(artists):
        return
