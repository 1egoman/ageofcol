import pygame
from pygame.locals import *

""" Miniture copy of the map """
class Minimap(object):

  def __init__(self, isoMap, Sx, Sy):
    self.Sx, self.Sy = Sx, Sy
    self.isoMap = isoMap
    self.averageTile = {}

    self.tileWidth = 32
    self.tileHeight = 16

    # create tile averages
    self.createTileColors()


  # Figures out if the event was over the minimap
  def isOver(self, event, screen):
    # get mouse coords
    Mx, My = event.pos

    # calculate our difference in offset between the real map and the minimap
    ratio = self.isoMap.tileWidth*1.0 / self.tileWidth
    Rx = int(self.isoMap.offsetX / ratio)
    Ry = int(self.isoMap.offsetY / ratio) - (self.isoMap.mapHeight / 2) * self.tileHeight
    Rw = int(screen.get_width() / ratio)
    Rh = int(screen.get_height() / ratio)

    # parse the screen coords
    Sx, Sy = self.getScreenPos(screen)

    # make sure the user clicked on the map
    if (Mx > Sx-Rw and Mx < Sx and My > Sy-Rw and My < Sy): return True
    else: return False



  # determines the average color for each tile
  def createTileColors(self):
    for k,v in self.isoMap.mapResources["tiles"].items():
      self.averageTile[k] = pygame.transform.average_color(v)
      


  def getScreenPos(self, screen):
    # calculate screen X pos
    if self.Sx < 0:
      Sx = screen.get_width() + self.Sx
    else:
      Sx = self.Sx

    # calculate screen Y pos
    if self.Sy < 0:
      Sy = screen.get_height() + self.Sy
    else:
      Sy = self.Sy

    return Sx, Sy


  # if a user clicks/drags on the map, move the view respectivly
  def dragOnMap(self, event, screen):
    
    # Used to calculate our difference in offset between the real map and the minimap
    ratio = self.isoMap.tileWidth*1.0 / self.tileWidth

    if self.isOver(event, screen):
      # get map rel coordinates
      Rx, Ry = event.rel

      # get the correct amount to move the map
      Dx = int( Rx * ratio )
      Dy = int( Ry * ratio )

      # lastly, actually move the map
      self.isoMap.offsetX += Dx
      self.isoMap.offsetY += Dy
      return True
      
    else:
      # user didn't click in correct area
      return False