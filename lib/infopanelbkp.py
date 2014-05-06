from common import common
from graphics import graphics
import pygame, os
from pygame.locals import *

class infopanel(object):
  line = [None]*10
  width = 400
  height = 100

  def render(self, x, y, font, imgs):
    pygame.draw.rect(common.screen, (100,100,100), (x, y, self.width, self.height))
    __, fh = font.size("a")
    twocolmoffset = 185
    if not common.selected or common.selected.health <= 0:
      toprint = self.line
      for cone in xrange(0, len(toprint)/2):
        txt = font.render(toprint[cone], True, (255,255,255))
        common.screen.blit(txt, (x+25, 6+y+(cone*fh)))
        common.screen.blit(imgs[cone], (x+5, 6+y+(cone*fh)))
      for ctwo in xrange(len(toprint)/2, len(toprint)):
        txt = font.render(toprint[ctwo], True, (255,255,255))
        common.screen.blit(txt, (x+twocolmoffset+25, 6+y+((ctwo-5)*fh)))
        common.screen.blit(imgs[ctwo], (x+twocolmoffset+5, 6+y+((ctwo-5)*fh)))
    else:
      selectedlist = []
      if common.selected.name: selectedlist.append("Name: "+common.selected.name)
      selectedlist.append("Type: "+common.selected.__class__.__name__)
      if common.selected.x and common.selected.y: selectedlist.append("Position: "+str(common.selected.x)+","+str(common.selected.y))
      if common.selected.owner: selectedlist.append("Owner(s): "+common.selected.owner)
      if common.selected.health and common.selected.maxhealth: selectedlist.append("Health: "+str(common.selected.health)+"/"+str(common.selected.maxhealth))
      if common.selected.hostile: 
        if common.selected.hostile == True: selectedlist.append("Hostile: Yes")
        if common.selected.hostile == False: selectedlist.append("Hostile: No")

      for cct,cline in enumerate(selectedlist):
        txt = font.render(cline, True, (255,255,255))
        common.screen.blit(txt, (x+25, 6+y+(cct*fh)))
        common.screen.blit(imgs[cct], (x+5, 6+y+(cct*fh))) 
  
  def setText(self, col, row, text):
    self.line[(col*5)+row] = text

