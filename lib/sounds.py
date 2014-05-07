#!/usr/bin/python
import common
import os
from os.path import join
import settings
import pygame

class sounds(object):

  musicdir = join(common.rootdir, "recources", "sounds", "music")  #location of music files
  sfxdir = join(common.rootdir, "recources", "sounds", "sfx")  #location of sound effect files

  musicnames = ["Into_the_Unknown"]
  musicfiles = [join(musicdir, m+".ogg") for m in musicnames]
  
  sfxnames = ["coins"]
  sfxfiles = [join(sfxdir, m+".ogg") for m in sfxnames]

  def __init__(self):
    pygame.mixer.init()

    self.Channel_Music = pygame.mixer.Channel(0)

    self.Channel_Sfx1 = pygame.mixer.Channel(1)
    self.Channel_Sfx2 = pygame.mixer.Channel(2)
    self.Channel_Sfx3 = pygame.mixer.Channel(3)
    self.Channel_Sfx4 = pygame.mixer.Channel(4)
    self.Channel_Sfx5 = pygame.mixer.Channel(5)



  #Play music
  def playmusic(self, music):
    self.Channel_Music.set_volume((common.mastervolumefactor*common.musicvolume)/2)  #Sets the volume of the music channel
    #TODO: put music&sfx channel volumes in game clock

    #Checks if song exists
    if music not in self.musicnames:
      return 0

    #Sets song to play
    for n in self.musicnames:
      if music == self.musicnames[len(n)]:
        musicsound = self.musicfiles[len(n)]
        break

    musicsound = pygame.mixer.Sound(musicsound)
    self.Channel_Music.play(musicsound, loops=-1, fade_ms=6000)  #plays on music channel, loops infinetly, fades in over specified time

    return 1


  #Stops currently playing music
  def stopmusic(self):
    self.Channel_Music.fadeout(4000)


  #Play sfx
  def playsfx(self, sfx):
    pass
    if sfx == sfx1:
      sfxsound = join(sfxdir, "2_coins.ogg")
    #elif sfx == ...:  #And so on...
    else:
      return 0

    sfxsound = pygame.mixer.Sound(sfxsound)
    sfxsound.set_volume((50)/2)  #Volume of sfx
    sfxsound.play(loops=0)  #Play sfx once
    sfxsound = None

    return 1

#Channel_Music.set_volume((common.mastervolumefactor*common.musicvolume)/2)
#Channel_Sfx1.set_volume((common.mastervolumefactor*common.sfxvolume)/2)