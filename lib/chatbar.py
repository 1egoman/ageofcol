import pygame, difflib
import common
from pygame.locals import *


class chatbox(object):
  x=0
  y=0
  w=0
  h=0
  fullh=0
  _ddselected=None
  listmatches = []
  hide = False
  txt=""
  cursorpos=1
  items = []

  def __init__(self,x,y,w,h):
    pygame.font.init()
    self._font = pygame.font.SysFont("freemono", 15)

    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def render(self, screen, x,y,w,h):
    if self.hide: return

    self.x = x
    self.y = y
    self.w = w
    self.h = h

    # Draw textbox
    pygame.draw.rect(screen, (255,255,255), (self.x,self.y,self.w,self.h))
    pygame.draw.rect(screen, (0,0,0), (self.x,self.y,self.w,self.h), 1)

    # Scroll text in textbox
    if self._font.size(self.txt+"_")[0] > self.w: 
      isize, _ = self._font.size("a")
      rndrtxt = self.txt[len(self.txt)-(self.w/isize-1):]+"_"
    else:
      rndrtxt = self.txt+"_"

    # Draw text
    r = self._font.render(rndrtxt, True, (0,0,0))
    screen.blit(r, (self.x+3,self.y+3))





    # Dropdown list; checks if this is enabled
    if common.suggestposts:
      # Compute the matching items
      if self.txt:
        self.listmatches = difflib.get_close_matches(self.txt, self.items)
      else:
        self.listmatches = self.items[:8]


      # Draw bg
      self.fullh = 5+len(self.listmatches)*20
      pygame.draw.rect(screen, (180,180,180), (self.x, self.y+self.h, self.w, self.fullh))

      # Draw matching items
      for c,i in enumerate(self.listmatches):
        r = self._font.render(i, True, (0,0,0))
        screen.blit(r, (self.x+5, self.y+self.h+5+c*20))




  def event(self, event):
    if self.hide: return

    # Do keypress
    if event.type == pygame.KEYDOWN:
      # print event.key
      if event.key == 8: 
        self.txt = self.txt[:-1]

      elif event.key == 27: # Esc Key
        self.txt = ""
        return False

      elif event.key == 13: # Return
        s = self.txt
        self.txt = ""
        return s

      elif event.key == 9: # tab
        self.txt = self.items[0]

      else:
        try:
          _ = chr(event.key)
          self.txt += event.unicode
        except ValueError: pass

    elif event.type == pygame.MOUSEBUTTONDOWN:
      mx, my = event.pos
      # The user clicked on the dropdown list
      if mx >= self.x and my >= self.y+self.h and mx <= self.x+self.w and my <= self.y+self.h+self.fullh-5:
        self._ddselected = ((my-self.y)/20)-1
        self.txt = self.listmatches[self._ddselected]