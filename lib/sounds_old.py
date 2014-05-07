#!/usr/bin/python
import common
import os
import settings
import pygame

musicdir = os.path.join(common.rootdir, "recources", "sounds", "music")  #location of music files
sfxdir = os.path.join(common.rootdir, "recources", "sounds", "sfx")  #location of sound effect files

song1 = "Into_the_Unknown"
sfx1 = "coins"


def checksoundname(soundname):  #checks if requested music or sfx name exists
	if soundname == song1:
		return 1
	elif soundname == sfx1:
		return 1
	#elif soundname == ...: #And so on...
	else:
		return 0


#Play music
def playmusic(music):
	if music == song1:  #Checks which song to play
		musicsound = os.path.join(musicdir, "Into_the_Unknown.ogg")
	#elif music == ...:  #And so on...

	else:
		return 0

	common.currentmusic = pygame.mixer.Sound(musicsound)
	common.currentmusic.set_volume((50)/2)  #Volume of music
	common.currentmusic.play(-1, fade_ms=8000)  #loops infinitely, fades in over specified time (in millisec)

	return 1


#Stops currently playing music
def stopmusic():
	common.currentmusic.stop()
	common.currentmusic = None


def playsfx(sfx):  #Play sfx
	if sfx == sfx1:
		sfxsound = os.path.join(sfxdir, "2_coins.ogg")
	#elif sfx == ...:  #And so on...

	else:
		return 0

	sfxsound = pygame.mixer.Sound(sfxsound)
	sfxsound.set_volume((50)/2)  #Volume of sfx
	sfxsound.play(loops=0)  #Play sfx once
	sfxsound = None

	return 1
