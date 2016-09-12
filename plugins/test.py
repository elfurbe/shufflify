#!/usr/bin/python

import abc

from danimate import shuffler

## This class represents a single song.
class Song:
    ## Constructor
    # @param title      The title of the song.
    # @param artist     The name of the artist who inflicted this audio on the world.
    # @param album      The album containing this blasphemy.
    # @param albumIndex The index of the song on the album.
    def __init__(self, title, artist, album, albumIndex):
        self.m_title      = title
        self.m_artist     = artist
        self.m_albumIndex = albumIndex
    
    ## Equality comparison
    # @param other The other Song object being compared
    # @return Returns true if the two objects are the same, false otherwise
    def __eq__(self, other):
        if m_title == other.m_title and m_artist == other.m_artist:
            return True
        else:
            return False
            
    ## Compare the artist only
    # @param other The other Song object being compared
    # @return True if the songs have the same artist.
    def sameArtist(self, other):
        if self.m_artist == other.m_artist:
            return True
        else:
            return False
    
    ## See if the input song is the next song on the same album
    # @param other Song to be used for comparison.
    # @return True if the input song is the next song on the same album
    def nextSong(self, other):
        if self.m_album == other.m_album and other.m_albumIndex == self.m_albumIndex + 1 and self.m_artist == other.m_artist:
            return True
        else:
            return False

#create a shuffler object
sh = shuffler()

#create a list of songs and artists
songList = []
songList.append(Song("Never Gonna Give You Up", "Rick Astley", "Fuck", 1))
songList.append(Song("Barbie Girl", "Aqua", "Shit", 2))
songList.append(Song("Some other horseshit", "Rick Astley", "Fuck", 2))

indices = sh.shuffle(songList)


