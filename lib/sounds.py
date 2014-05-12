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
    self.setvolumes()

    #Sets and plays song
    for m in self.musicnames:
      if music == m:
        self.musicsound = self.musicfiles[self.musicnames.index(m)]
        self.musicsound = pygame.mixer.Sound(self.musicsound)
        self.Channel_Music.play(self.musicsound, loops=-1, fade_ms=10000)  #plays music infinite times, fades in over specified time in millisec
        break



  #Play sfx
  def playsfx(self, sfx):
    self.setvolumes()

    #Sets sfx to play
    for s in self.sfxnames:
      if sfx == s:
        self.sfxsound = self.sfxfiles[self.sfxnames.index(s)]
        self.sfxsound = pygame.mixer.Sound(self.sfxsound)
        break

    #Finds a free channel
    if not self.Channel_Sfx1.get_busy():
      self.Channel_Sfx1.play(self.sfxsound, loops=0)

    elif not self.Channel_Sfx2.get_busy():
      self.Channel_Sfx2.play(self.sfxsound, loops=0)

    elif not self.Channel_Sfx3.get_busy():
      self.Channel_Sfx3.play(self.sfxsound, loops=0)

    elif not self.Channel_Sfx4.get_busy():
      self.Channel_Sfx4.play(self.sfxsound, loops=0)

    elif not self.Channel_Sfx5.get_busy():
      self.Channel_Sfx5.play(self.sfxsound, loops=0)

    else:
      print ("All SFX Channels Busy")




  def setvolumes(self):
    self.Channel_Music.set_volume((common.mastervolume/100.00)*(common.musicvolume/100.00))

    self.Channel_Sfx1.set_volume((common.mastervolume/100.00)*(common.sfxvolume/100.00))
    self.Channel_Sfx2.set_volume((common.mastervolume/100.00)*(common.sfxvolume/100.00))
    self.Channel_Sfx3.set_volume((common.mastervolume/100.00)*(common.sfxvolume/100.00))
    self.Channel_Sfx4.set_volume((common.mastervolume/100.00)*(common.sfxvolume/100.00))
    self.Channel_Sfx5.set_volume((common.mastervolume/100.00)*(common.sfxvolume/100.00))