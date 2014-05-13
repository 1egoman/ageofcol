#!/usr/bin/python
import common
import os
import pygame
from pygame.locals import *
import economy
import ai
import entity
import textwrap
import sounds

global posts
posts = []

common.sounds = sounds.sounds()

def run(command):

  system = "system"
  player = "player"

  if command[0] == "/":
    words = command.split(" ")
    cmd = words[0]
    args = words[1:]

    if cmd == "/help" or cmd == "/?":
      post(system, "TODO: add some help!")


    elif cmd == "/debug":
      if common.debugcommands == True:
        common.debugcommands = False
        post(system, "Disabling Debug Commands.")
      elif common.debugcommands == False:
        common.debugcommands == True
        post(system, "WARNING: Debug Commands Enabled. Improper Command Syntax Will Result in Crashes.")




    elif cmd == "/kill":
      if common.selected and common.selected.health:

        common.selected.health = 0
        post(system, "Killed "+str(common.selected))
        common.selected = None

      else:
        post(system, "Please Select a Mob First!")





    elif cmd == "/give":
      if common.selected and common.selected.health and hasattr(common.selected, "inventory"):
        try:
          f = entity.entity.itemsbyid[int(args[0])]

          if len(args) == 0:
            amt = 10
          else:
            amt = int(args[1])

          common.selected.inventory.additem(int(args[0]), amt)
          post(system, "Gave Item.")
          common.selected = None

        except KeyError:
          post(system, "Item Doesn't Exist")

        except IndexError:
          try:
            args[0]
          except IndexError:
            post(system, "No Item Specified")

          try:
            args[1]
          except IndexError:
            post(system, "No Amount Specified")


      else:
        post(system, "Please Select a Mob First!")



    elif cmd == "/pay":
      try:
        if common.selected and common.selected.health and hasattr(common.selected, "wallet"):
          economy.pay(common.selected.wallet, int(args[0]))
          post(system, "Paid.")
          common.selected = None

        else:
          post(system, "Please Select a Mob First!")

      except IndexError:
        post(system, "Please Specify an Amount!")


    #TODO: add ability to specify spawn location
    elif cmd == "/spawn":
      try:
        if args[0] == "unit":
          common.ai.mobins.append(ai.unit(t=common.username,x=50,y=50))

        elif args[0] == "pig":
          common.ai.mobins.append(ai.pig(x=50,y=50))

        elif args[0] == "cow":
          common.ai.mobins.append(ai.cow(x=50,y=50))

        elif args[0] == "vulture":
          common.ai.mobins.append(ai.vulture(x=50,y=50))

        elif args[0] == "frog":
          common.ai.mobins.append(ai.frog(x=50,y=50))

        else:
          post(system, "Unknown Mob Type")


      except IndexError:
        try:
          args[0]
        except IndexError:
          post(system, "No Mob Specified")



    #NOTE: debug commands in following block; improper use will likely cause crashes
    elif common.debugcommands == True:

      #Change username
      if cmd == "/changeusername":
        if args[0] != common.sysname:
          common.username = args[0]
        else:
          post(system, "\"" + args[0] + "\" Cannot Be Used as Username")

      #Set master/music/sfx volume until settings implemented version
      elif cmd == "/mtvol":
        common.mastervolume = float(args[0])
        common.sounds.setvolumes()
        post(system, "Master Volume: " + str(common.mastervolume))

      elif cmd == "/mscvol":
        common.musicvolume = float(args[0])
        common.sounds.setvolumes()
        post(system, "Music Volume: " + str(common.musicvolume))

      elif cmd == "/sfxvol":
          common.sfxvolume = float(args[0])
          common.sounds.setvolumes()
          post(system, "Sound Effects Volume: " + str(common.sfxvolume))

      else:
        post(system, "Unknown Command. Run \"/help\" for Help.")




    else:
      post(system, "Unknown Command. Run \"/help\" for Help.")


  else:
    # Just talk
    post(player, command)



def post(whosays, string):
  if whosays == "system":
    string = "["+common.sysname+"] " + string

  elif whosays == "player":
    string = "["+common.username+"] " + string

  else:
    string = "[UNSPECIFIED WHOSAYS]" + string

  string = textwrap.wrap(string, width=common.maxpostlength)
  for p in string:
    posts.append(p)


def renderPosts():
  if common.activetool == "inventory": return
  width, height = 300, 10+len(posts)*20

  # pygame.draw.rect(common.screen, (180,180,180), (5, 5, width, height))
  if common.reverseposts: posts.reverse()

  for c,i in enumerate(posts[:common.maxposts]):
    r = common.g.font.render(i, True, (0,0,0))
    #common.screen.blit(r, (10, 10+c*20))
    common.screen.blit(r, (10, common.height-45-c*20))

  if common.reverseposts: posts.reverse()