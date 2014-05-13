import pygame
from pygame.locals import *

from math import *
import os
import json


""" Basically, a class that handes all the map related stuff and the math behind it all """
class isoMap(object):


  def __init__(self, surface, mapWidth, mapHeight, tileWidth=128, tileHeight=64):

    # surface
    self._s = surface

    # generate map
    self.mapWidth = mapWidth
    self.mapHeight = mapHeight
    self._tiles = [   [ {"name": "grass"} for _ in xrange(0, mapHeight) ] for _ in xrange(0, mapWidth)   ]
    self._tiles[0][0]["name"] = "water"

    # tile size
    self.tileWidth = tileWidth
    self.tileHeight = tileHeight

    # map offset
    self.offsetX = 0
    self.offsetY = 0

    # file resources
    self.mapResources = { "tiles": {} }
    self.loadAllResources()

    # map info
    self.mapName = "Untitled"
    self.mapAuthor = "Anonymous"
    self.mapDesc = "A new map"

    # selection
    self.selection = None

    # other
    self.renderBorders = 0


  # loads all resources for game to work
  def loadAllResources(self, location="res"):
    tile = os.path.join( os.path.abspath(location), "tiles" )

    # load in all tiles
    for f in os.listdir(tile):
      name = f.split('.')[0]
      self.mapResources["tiles"][name] = pygame.image.load( os.path.join(tile, f) ).convert_alpha()



  # draws the map to the screen
  def drawMap(self):

    # loop through each tile
    for i in xrange(self.mapWidth-1, -1, -1):
      for j in xrange(0, self.mapHeight):

        # get tile position
        Cx, Cy = self.IsoToScreen(i, j)



        # get tile name, and respective surface
        tileName = self._tiles[i][j]["name"]
        tileSurface = self.mapResources["tiles"][tileName]

        # get surface's position
        Tx = Cx + self.offsetX
        Ty = Cy + self.offsetY - tileSurface.get_height() + self.tileHeight + self.tileHeight/4

        # draw the tile
        self._s.blit(tileSurface, (Tx, Ty))


        # render borders
        if self.renderBorders:

          # create the iso tile shape
          tilePoints = [
            (self.offsetX + Cx+self.tileWidth/2, self.offsetY + Cy),
            (self.offsetX + Cx+self.tileWidth,   self.offsetY + Cy+self.tileHeight/2),
            (self.offsetX + Cx+self.tileWidth/2, self.offsetY + Cy+self.tileHeight),
            (self.offsetX + Cx,                  self.offsetY + Cy+self.tileHeight/2)
          ]

          # draw the border
          pygame.draw.polygon(self._s, (0, 0, 0), tilePoints, 1)


    # draw selection area
    if self.selection:

      # make sure that the selection can never reach zero in size
      if self.selection[2] == 0: self.selection[2] = 1
      if self.selection[3] == 0: self.selection[3] = 1

      # this calculates the correct iterator to use in the for loop
      # depending on if the size of the x selection is positive or negitive
      if self.selection[2] > 0:
        iterX = xrange(self.selection[2]-1, -1, -1)
      else:
        iterX = xrange(self.selection[2]-1, 1, 1)


      # this calculates the correct iterator to use in the for loop
      # depending on if the size of the y selection is positive or negitive
      if self.selection[3] > 0:
        iterY = xrange(0, self.selection[3], 1)
      else:
        iterY = xrange(0, self.selection[3], -1)



      # loop through tiles
      for i in iterX:
        for j in iterY:

          # get tile position
          Cx, Cy = self.IsoToScreen( self.selection[0] + i, self.selection[1] + j )

          # create the iso tile shape
          tilePoints = [
            (self.offsetX + Cx+self.tileWidth/2, self.offsetY + Cy),
            (self.offsetX + Cx+self.tileWidth,   self.offsetY + Cy+self.tileHeight/2),
            (self.offsetX + Cx+self.tileWidth/2, self.offsetY + Cy+self.tileHeight),
            (self.offsetX + Cx,                  self.offsetY + Cy+self.tileHeight/2)
          ]

          # draw the border
          pygame.draw.polygon(self._s, (10, 158, 191), tilePoints, 4)


  # converts isometric coords into 2d screen coordinates
  def IsoToScreen(self, x, y):
    screenX = (y+x)*(self.tileWidth/2)
    screenY = (y-x)*(self.tileHeight/2)
    return screenX, screenY


  # converts 2d screen coords into isometric coordinates
  def screenToIso(self, x, y):
    x, y = x*1.0-self.tileHeight/2, y*1.0
    tx = (y - x/2)/self.tileHeight
    ty = (y + x/2)/self.tileHeight
    return -floor(tx), floor(ty)


  # loads a map from a map folder
  def loadMap(self, levelfolder="maps/default"):

    # get map path
    mapPath = os.path.abspath(levelfolder)

    # load map info
    infoPath = os.path.join(mapPath, "info.json")
    with open(infoPath, 'r') as f:
      infoStuffs = json.loads( f.read() )

      # set information
      if infoStuffs.has_key("name"): 
        self.mapName = infoStuffs["name"]

      if infoStuffs.has_key("author"): 
        self.mapAuthor = infoStuffs["author"]

      if infoStuffs.has_key("desc"): 
        self.mapDesc = infoStuffs["desc"]


    # load the map itself
    tilesPath = os.path.join(mapPath, "map.json")
    with open(tilesPath, 'r') as f:
      tileStuffs = json.loads( f.read() )

      # load into tiles array
      if tileStuffs.has_key("tiles"):

        self.mapWidth = len(tileStuffs["tiles"])
        self.mapHeight = len(tileStuffs["tiles"][0])
        self._tiles = tileStuffs["tiles"]