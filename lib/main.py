#!/usr/bin/python
import sys
import os
import json

import common
import launcher
import settings
import sounds
from events import *
from graphics import *
from entity import entity
from ai import ai
from infopanel import infopanel
from structures import *
from inventory import playertotals
from panel import morepanel
from chatbar import chatbox

import pygame
from pygame.locals import *


hand_str = [
  "     ..         ",
  "    .xx.        ",
  "    .xx.        ",
  "    .xx.        ",
  "    .xx.....    ",
  "    .xx.xx.x..  ",
  " .. .xx.xx.x.   ",
  ".xx..xxxxxxxxx. ",
  ".xxx.xxxxxxxxx. ",
  " .xx.xx.x.x.xx. ",
  "  .xxxx.x.x.xx. ",
  "  .xxxx.x.x.x.  ",
  "   .xxx.x.x.x.  ",
  "    .xxxxxxx.   ",
  "     .xxxx.x.   ",
  "     ..... ..   "
]

grabber_str = [
  "                ",
  "                ",
  "                ",
  "                ",
  "     .......    ",
  "    .xx.xx.x..  ",
  " .. .xx.xx.x.   ",
  ".xx..xxxxxxxxx. ",
  ".xxx.xxxxxxxxx. ",
  " .xx.xx.x.x.xx. ",
  "  .xxxx.x.x.xx. ",
  "  .xxxx.x.x.x.  ",
  "   .xxx.x.x.x.  ",
  "    .xxxxxxx.   ",
  "     .xxxx.x.   ",
  "     ..... ..   "
]





class main(object):

  def onexecute(self):

    # make an instance of all the functions
    # common.c = common()
    common.inventorytotal = playertotals()
    common.mp = morepanel()
    common.e = event()
    common.ai = ai()
    common.ip = infopanel()
    common.en = entity()
    common.cv = civilization()
    common.g = graphics()
    common.sounds = sounds.sounds()

    # initialize pygame
    pygame.init()


    # Read from config file
    opt = open(os.path.join(common.rootdir, "options.json"), 'r')
    y = json.loads(opt.read())
    common.srclocation = os.path.join("texturepacks", y['texturepack'])
    common.enablesky = bool(y['sky'])
    opt.close()

    # load the window
    common.screen = pygame.display.set_mode( (common.width, common.height), RESIZABLE)
    pygame.display.set_caption(common.name+" v."+str(common.version));
    common.running = True
    common.screen.fill((255,255,255))

    # load all images/resources
    common.g.loadall()
    pygame.display.set_icon(civilization.buildingtextures[0])

    # do cursors
    common.hand = pygame.cursors.compile(hand_str, 'x', '.', "o")
    common.grabber = pygame.cursors.compile(grabber_str, 'x', '.', "o")

    #Starts music
    common.sounds.playmusic("Into_the_Unknown")

    self.fromlauncher()

  def fromlauncher(self):
    # Do launcher Stuff.....
    if not common.bypasslauncher: 
      l = launcher.launcher()
      if common.running: l.renderLoadingScreen()
    if common.inlauncher == True: self.cleanup()

    # Load world
    graphics.level = levelparser.level(os.path.join(common.rootdir, "saves", common.levelname, "level.json"))
    common.g.tilemap = graphics.level.parseTiles()

    common.maph = len(common.g.tilemap[0])*common.tilewidth
    common.mapw = len(common.g.tilemap)*common.tilewidth

    # Initialize pause menu
    common.pausemenu = settings.pausemenu()


    # Create the chatbox
    common.cb = chatbox(10,common.height-25,500,20)
    common.cb.hide = True

    # go to mainloop
    self.loop()

  def loop(self):
    pygame.time.set_timer(pygame.USEREVENT+1, common.keyreadpersec)
    pygame.time.set_timer(pygame.USEREVENT+2, 100)

    common.clock = pygame.time.Clock()
    common.g.drawFromConfig()

    while common.running:
      common.clock.tick(common.fps)
      for event in pygame.event.get():
        common.e.newevent(event)
      # TODO: insert mainloop code
      common.g.render()
    common.running = False
    self.cleanup()

  def cleanup(self):

    if common.quitToLauncher: 
      common.quitToLauncher = False
      common.running = True
      common.inlauncher = False
      self.fromlauncher()

    pygame.time.set_timer(pygame.USEREVENT+1, 0)
    sys.exit(0)

if __name__ == '__main__':
  m = main()
  m.onexecute()