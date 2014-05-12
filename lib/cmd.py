#!/usr/bin/python
import common
import os
import pygame
from pygame.locals import *
import economy
from ai import unit
import entity
import sounds

global posts
posts = []

common.sounds = sounds.sounds()

def run(command):

  if command[0] == "/":
    words = command.split(" ")
    cmd = words[0]
    args = words[1:]

    if cmd == "/help" or cmd == "/?":
      post("TODO: add some help!")
      post("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")




    elif cmd == "/kill":
      if common.selected and common.selected.health:

        common.selected.health = 0
        post("Killed "+str(common.selected))
        common.selected = None

      else:
        post("Please Select a Mob First!")





    elif cmd == "/give":
      if common.selected and common.selected.health and hasattr(common.selected, "inventory"):
        try:
          f = entity.entity.itemsbyid[int(args[0])]

          if len(args) == 0:
            amt = 10
          else:
            amt = int(args[1])

          common.selected.inventory.additem(int(args[0]), amt)
          post("Gave Item.")
          common.selected = None

        except KeyError:
          post("Item Doesn't Exist")



      else:
        post("Please Select a Mob First!")


    elif cmd == "/pay":
      if common.selected and common.selected.health and hasattr(common.selected, "wallet"):
        economy.pay(common.selected.wallet, int(args[0]))
        post("Paid.")
        common.selected = None

      else:
        post("Please Select a Mob First!")

    elif cmd == "/spawn":
      if args[0] == "unit":
        unit(common.username,50,50)
      else:
        post("Unknown Mob Type")


    elif cmd == "/changeusername":
      common.username = args[0]


    #Set master/music/sfx volume until settings implemented version
    elif cmd == "/mtvol":
      common.mastervolume = float(args[0])
      common.sounds.setvolumes()
      post("Master Volume: " + str(common.mastervolume))

    elif cmd == "/mscvol":
      common.musicvolume = float(args[0])
      common.sounds.setvolumes()
      post("Music Volume: " + str(common.musicvolume))

    elif cmd == "/sfxvol":
      common.sfxvolume = float(args[0])
      common.sounds.setvolumes()
      post("Sound Effects Volume: " + str(common.sfxvolume))





    else:
      post("Unknown Command. Run /help for Help.")

  else:
    # Just talk
    post("["+common.username+"] "+command)



def post(string): posts.append(string)


def renderPosts():
  if common.activetool == "inventory": return
  width, height = 300, 10+len(posts)*20

  # pygame.draw.rect(common.screen, (180,180,180), (5, 5, width, height))
  if common.reverseposts: posts.reverse()

  for c,i in enumerate(posts[:common.maxposts]):
    r = common.g.font.render(i, True, (0,0,0))
    common.screen.blit(r, (10, 10+c*20))

  if common.reverseposts: posts.reverse()