import pygame
from pygame.locals import *
import os


# holds previous selection
prevSelection = None

# currently active dialog
activeDialog = None


# check if the selection has changed, and if nessisary spawn a new dialog
def checkToSpawnDialog(isoMap):
  global prevSelection, activeDialog

  # compare
  if isoMap.selection != prevSelection and isoMap.selection:
    # spawn new dialog
    activeDialog = SelectionDialog(isoMap, *isoMap.selection)
    prevSelection = isoMap.selection

  elif isoMap.selection != prevSelection:
    activeDialog = None
    prevSelection = None


  if activeDialog:
    activeDialog.dX = 8#isoMap.selection[0]#
    activeDialog.dY = 8#isoMap.selection[1]# + isoMap.offsetY
    # activeDialog.computeLocation()



# draw the active dialog, if there is one
def drawDialog(screen):
  if activeDialog:
    activeDialog.draw(screen)
    return 1
  else:
    return 0





""" Onscreen information display for user """
class Dialog(object):

  def __init__(self, m, x, y, w, h):
    self.oX, self.oY = x, y
    self.oW, self.oH = w, h
    self.isoMap = m
    self.computeLocation()

  # compute draw location (roughly for now)
  def computeLocation(self):
    oX, oY = self.isoMap.IsoToScreen(self.oX + self.oW/2, self.oY + self.oH/2)
    self.dX = oX + self.isoMap.offsetX
    self.dY = oY + self.isoMap.offsetY + self.isoMap.tileHeight/2

  def draw(self, screen):
    # draw dialog
    # pygame.draw.rect(self.isoMap.s, (255, 0, 0), (self.dX, self.dY, 200, 100))
    pygame.draw.rect(screen, (255, 0, 0), (self.dX, self.dY, 200, 100))



""" Shows info about selected item"""
class SelectionDialog(Dialog):

  DLG_WIDTH = 400
  DLG_HEIGHT = 200

  def __init__(self, *args):
    super(SelectionDialog, self).__init__(*args)

    # load the images that we need
    location="res"
    entitydlg = os.path.join( os.path.abspath(location), "dialogs", "entityinfo.png")
    self.Image = pygame.image.load(entitydlg).convert_alpha()

    # used to show health
    self.Heart = pygame.Surface((48,48), SRCALPHA)
    self.Heart.blit(self.Image, (0, 0), (self.DLG_WIDTH, 0, 48, 48))

    # fonts
    self.titleFont = pygame.font.SysFont(pygame.font.get_default_font(), 36)
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 18)


  def draw(self, screen):

    # render the dialog only if some object is selected
    if self.isoMap.selectedItems:
      selectedItem = self.isoMap.selectedItems[0]

      # draw dialog
      screen.blit(self.Image, (self.dX, self.dY), (0, 0, self.DLG_WIDTH, self.DLG_HEIGHT))

      # get entities name
      if hasattr(selectedItem, "name"):
        selectedName = selectedItem.name
      else:
        selectedName = selectedItem.__class__.__name__

      # render name (upper left)
      title = self.titleFont.render(selectedName, 1, (255, 255, 255))
      screen.blit(title, (self.dX+8, self.dY+12))

      # render health (as hearts in upper right)
      selectedHealth = selectedItem.health
      for h in xrange( 0, int(selectedHealth*4) ):  # 4 = 4 hearts total
        hX = self.dX + self.DLG_WIDTH/2 + h*self.Heart.get_width()
        screen.blit(self.Heart, (hX, self.dY))

      # get some other stats
      toOutput = []

      # owner
      if hasattr(selectedItem, "owner"):
        allOwners = "Owner(s): " + ", ".join( selectedItem.owner )
        toOutput.append( allOwners )

      # population
      if hasattr(selectedItem, "population"):
        allOwners = "Population: %s" % selectedItem.population
        toOutput.append( allOwners )



      # draw all those lines in toOutput
      for c,i in enumerate(toOutput):

        # render text
        rndr = self.font.render(i, 1, (255,255,255))

        # calculate position of the line
        # 48 = top header height, 8 = margin
        Lx = self.dX + 8
        Ly = self.dY + 48 + 8 + c*rndr.get_height()

        # draw it
        screen.blit(rndr, (Lx, Ly))