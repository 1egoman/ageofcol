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



  # determines the average color for each tile
  def createTileColors(self):
    for k,v in self.isoMap.mapResources["tiles"].items():
      self.averageTile[k] = pygame.transform.average_color(v)


  # renders the minimap
  def draw(self):


    # y offset so that it will render in the right place
    Yoff = (self.isoMap.mapHeight * self.tileHeight)/2

    # calculate our difference in offset, and size
    ratio = self.isoMap.tileWidth*1.0 / self.tileWidth
    Rx = int(self.isoMap.offsetX / ratio)
    Ry = int(self.isoMap.offsetY / ratio) - (self.isoMap.mapHeight / 2) * self.tileHeight
    Rw = int(self.isoMap.s.get_width() / ratio)
    Rh = int(self.isoMap.s.get_height() / ratio)


    # parse the screen coords
    Sx, Sy = self.getScreenPos()


    # create surface to draw upon
    mapSurf = pygame.Surface((Rw, Rh), SRCALPHA)
    mapSurf.fill((96, 96, 96, 200))

    # loop through each tile
    for i in xrange(self.isoMap.mapWidth-1, -1, -1):
      for j in xrange(0, self.isoMap.mapHeight): 

        # convert iso coords to screen coords
        Cx = (j+i)*(self.tileWidth/2)
        Cy = (j-i)*(self.tileHeight/2)

        # get the isometric shape
        tilePoints = [
          (Rx + Cx+self.tileWidth/2, Ry + Yoff + Cy),
          (Rx + Cx+self.tileWidth,   Ry + Yoff + Cy+self.tileHeight/2),
          (Rx + Cx+self.tileWidth/2, Ry + Yoff + Cy+self.tileHeight),
          (Rx + Cx,                  Ry + Yoff + Cy+self.tileHeight/2)
        ]

        # get tile name
        tileName = self.isoMap._tiles[i][j]["name"]

        # find the tile's color
        color = list( self.averageTile[tileName][:3] )
        color.append(200) # set alpha

        # render tile
        pygame.draw.polygon(mapSurf, color, tilePoints)



    # draw Map to the screen
    self.isoMap.s.blit(mapSurf, (Sx-Rw, Sy-Rh))

    # draw border
    pygame.draw.rect(self.isoMap.s, (64, 64, 64), (Sx-Rw, Sy-Rh, Rw, Rh), 4)



  def getScreenPos(self):
    # calculate screen X pos
    if self.Sx < 0:
      Sx = self.isoMap.s.get_width() + self.Sx
    else:
      Sx = self.Sx

    # calculate screen Y pos
    if self.Sy < 0:
      Sy = self.isoMap.s.get_height() + self.Sy
    else:
      Sy = self.Sy

    return Sx, Sy


  # if a user clicks/drags on the map, move the view respectivly
  def dragOnMap(self, event):
    
    # get mouse coords
    Mx, My = event.pos

    # calculate our difference in offset between the real map and the minimap
    ratio = self.isoMap.tileWidth*1.0 / self.tileWidth
    Rx = int(self.isoMap.offsetX / ratio)
    Ry = int(self.isoMap.offsetY / ratio) - (self.isoMap.mapHeight / 2) * self.tileHeight
    Rw = int(self.isoMap.s.get_width() / ratio)
    Rh = int(self.isoMap.s.get_height() / ratio)

    # parse the screen coords
    Sx, Sy = self.getScreenPos()

    # make sure the user clicked on the map
    if (Mx > Sx-Rw and Mx < Sx and My > Sy-Rw and My < Sy):

      # get map rel coordinates
      Rx, Ry = event.rel

      # get the correct amount to move the map
      Dx = int( Rx * ratio )
      Dy = int( Ry * ratio )

      # lastly, actually move the map
      self.isoMap.offsetX += Dx
      self.isoMap.offsetY += Dy
      return 1
      
    else:
      # user didn't click in correct area
      return 0