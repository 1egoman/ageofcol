import common
import genmap
import easygui
import shutil

import pygame
import os
import json
from pygame.locals import *
from listbox import listdisplay

class launcher(object):
  path = 'http://geekling.us/aoc/version/version.json'

  def __init__(self):
    common.inlauncher = True
    self.playerx = 0
    self.playery = 0
    self.offset = 0
    self.loggedin = False
    self.voffset = 0
    self.vmaxheight = 0

    try:
      import urllib2
      self.json = json.loads( urllib2.urlopen(self.path).read() )
    except IndexError, urllib2.URLERROR:
      self.json = [{'ERROR: CANNOT FETCH VERSIONS FILE': []}]

    self.loop()

  def loop(self):
    self.loadresources()

    levels = [d for d in os.listdir(os.path.join(common.rootdir, "saves"))]
    self.l = listdisplay(common.screen, 5, 160, 200, 500, levels)


    common.clock = pygame.time.Clock()
    while common.running and common.inlauncher:

      common.clock.tick(common.fps)
      for event in pygame.event.get(): self.newevent(event)
      # TODO: insert mainloop code

      if self.loggedin:
        self.render()
      else:
        self.loginrender()


    # Return back to the mainloop to start the game





  def loginrender(self):
    # Draw a bg color
    common.screen.fill((100,100,100))

    # Draw sky over the whole screen
    for dx in xrange(0, common.width, common.g.sky.get_width()):
      for dy in xrange(0, common.height, common.g.sky.get_height()):
        common.screen.blit(common.g.sky, (dx, dy))

    font = pygame.font.SysFont('monospace', 12)
    bigfont = pygame.font.SysFont('monospace', 20)
    titlefont = pygame.font.SysFont('monospace', 50)


    # Draw logo
    common.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(common.rootdir, common.srclocation, "logo.png")).convert_alpha(), (500,150)), (60,5))

    # Draw version updates
    pygame.draw.rect(common.screen, (120,120,120), (50,150,common.width, common.height))

    versioncolor = (0,0,0)
    sectionheight = 200
    for ct,version in enumerate(self.json):

      common.screen.blit(bigfont.render(str(version.items()[0][0]), True, versioncolor), (75, sectionheight*ct+175+self.voffset))
      pygame.draw.line(common.screen, versioncolor, (75, sectionheight*ct+160+self.voffset), (325, sectionheight*ct+160+self.voffset))
      for c,i in enumerate(version.items()[0][1]):
        # print version.items()[0]
        rndr = font.render("- "+str(i), True, versioncolor)
        common.screen.blit(rndr, (140,(sectionheight*ct)+(c*15)+175+self.voffset))

    self.vmaxheight = (sectionheight*ct)+(c*15)+175+10


    # Draw the logo centered
    # common.screen.blit(self.logo, (lx,ly))

    pygame.display.flip()





  def render(self):

    # Draw a bg color
    common.screen.fill((100,100,100))

    # Draw sky over the whole screen
    for dx in xrange(0, common.width, common.g.sky.get_width()):
      for dy in xrange(0, common.height, common.g.sky.get_height()):
        common.screen.blit(common.g.sky, (dx, dy))

    font = pygame.font.SysFont('monospace', 12)
    bigfont = pygame.font.SysFont('monospace', 20)
    titlefont = pygame.font.SysFont('monospace', 50)

    # Draw logo
    common.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(common.rootdir, common.srclocation, "logo.png")).convert_alpha(), (500,150)), ((common.width-500)/2,5))

    m = self.l.x+self.l.w+(common.width-400)
    self.l.render()
    pygame.draw.rect(common.screen, (120,120,120), (self.l.x+self.l.w+5,self.l.y-2,common.width-400, self.l.h))
    
    # Render World Info
    try:
      rndr = titlefont.render(self.l.list[self.l.selecteditem], True, (255,255,255))
      common.screen.blit(rndr, (self.l.x+self.l.w+20, self.l.y+20))
    except IndexError:
      pass


    pygame.draw.rect(common.screen, (100,100,100), (self.l.x+self.l.w+(common.width-400)-150, self.l.y+3, 150, 50))
    pygame.draw.rect(common.screen, (100,100,100), (self.l.x+self.l.w+(common.width-400)-150, self.l.y+63, 150, 50))
    pygame.draw.rect(common.screen, (100,100,100), (self.l.x+self.l.w+(common.width-400)-150, self.l.y+123, 150, 50))

    # Load World Button
    rndr = bigfont.render("Load...", True, (255,255,255))
    common.screen.blit(rndr, (self.l.x+self.l.w+(common.width-400)-135, self.l.y+8))
    pygame.draw.lines(common.screen, (255,255,255), False, 
      [(m-135, self.l.y+40), (m-15, self.l.y+40), (m-30, self.l.y+35), (m-15, self.l.y+40), (m-30, self.l.y+45)])

    # New World Button
    rndr = bigfont.render("New...", True, (255,255,255))
    common.screen.blit(rndr, (self.l.x+self.l.w+(common.width-400)-135, self.l.y+68))

    # Del World Button
    rndr = bigfont.render("Delete...", True, (255,255,255))
    common.screen.blit(rndr, (self.l.x+self.l.w+(common.width-400)-135, self.l.y+128))

    pygame.display.flip()


  def renderLoadingScreen(self):
    for dx in xrange(0, common.width, common.tilewidth):
      for dy in xrange(0, common.height, common.tilewidth):
        common.screen.blit(common.g.grass, (dx, dy))

    r = common.g.largefont.render("Please Wait...", True, (255,255,255))
    common.screen.blit(r, ((common.width-r.get_width())*0.5,50))

    r = common.g.font.render("Loading of a world could take up to as much as 20 seconds.", True, (255,255,255))
    common.screen.blit(r, ((common.width-r.get_width())*0.5,80))

    pygame.display.flip()



  def loadresources(self):
    # Logo for the game
    # self.logo = pygame.transform.scale(pygame.image.load(os.path.join(common.rootdir, "src", "launcher", "logo.png")), (500,200)).convert_alpha()
    # self.guy = pygame.transform.scale(pygame.image.load(os.path.join(common.rootdir, "src", "launcher", "guy.png")), (common.tilewidth,common.tilewidth)).convert_alpha()
    pass

  def newevent(self, event):
    # Quit if needed
    if event.type == pygame.QUIT:
      common.running = False

    # Also, resize the screen
    elif event.type == pygame.VIDEORESIZE:
      # set width and height, then resize window
      common.width = event.w
      common.height = event.h
      common.screen = pygame.display.set_mode((common.width, common.height), RESIZABLE)
      self.render()

    # For now, quit launcher
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mx, my = event.pos
      if event.button == 1:

        if self.loggedin:
          # select world
          if mx <= self.l.x+self.l.w:
            self.l.event(event)

          elif my >= self.l.y+3 and my <= self.l.y+53 and mx >= self.l.x+self.l.w+(common.width-400)-150 and mx <= self.l.x+self.l.w+(common.width-400):

            common.levelname = self.l.list[self.l.selecteditem]
            common.inlauncher = False

          elif my >= self.l.y+63 and my <= self.l.y+113 and mx >= self.l.x+self.l.w+(common.width-400)-150 and mx <= self.l.x+self.l.w+(common.width-400):
            # new world
            name = genmap.makeMap()
            if name:
              # self.l.list = [d for d in os.listdir(os.path.join(common.rootdir, "saves"))]
              common.levelname = name
              common.inlauncher = False

          elif my >= self.l.y+123 and my <= self.l.y+173 and mx >= self.l.x+self.l.w+(common.width-400)-150 and mx <= self.l.x+self.l.w+(common.width-400):
            if easygui.ynbox("Really Delete World?", "", ("Yes", "No")):
              shutil.rmtree(os.path.join(common.rootdir, "saves", self.l.list[self.l.selecteditem]))
              self.l.list = [d for d in os.listdir(os.path.join(common.rootdir, "saves"))]

        else:
          self.loggedin = True

      elif not self.loggedin:

        if event.button == 4:
          self.voffset += 20
          if self.voffset >= 0: self.voffset = 0

        elif event.button == 5:
          self.voffset -= 20
          if self.voffset <= -self.vmaxheight: self.voffset = 0
