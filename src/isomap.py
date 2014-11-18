import pygame
from pygame.locals import *

from math import *
import os
import json

from entity import Entity, loadEntitesFromMap
from dialogSpawner import checkToSpawnDialog, drawDialog



""" Basically, a class that handes all the map related stuff and the math behind it all """
class isoMap(object):


  def __init__(self, mapWidth, mapHeight, tileWidth=128, tileHeight=64):
    # generate map
    self.mapWidth = mapWidth
    self.mapHeight = mapHeight
    self._tiles = [   [ {"name": "grass"} for _ in xrange(0, mapHeight) ] for _ in xrange(0, mapWidth)   ]

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

    # entity list
    self.entityList = []

    # other
    self.renderBorders = 0
    self.selection = None
    self.selectedItems = []


  # loads all resources for game to work
  def loadAllResources(self, location="res"):
    tile = os.path.join( os.path.abspath(location), "tiles" )

    # load in all tiles
    for f in os.listdir(tile):
      name = f.split('.')[0]
      self.mapResources["tiles"][name] = pygame.image.load( os.path.join(tile, f) ).convert_alpha()


  # converts isometric coords into 2d screen coordinates
  def IsoToScreen(self, x, y):
    screenX = (y+x)*(self.tileWidth/2)
    screenY = (y-x)*(self.tileHeight/2)
    return screenX, screenY


  # converts 2d screen coords into isometric coordinates
  def screenToIso(self, x, y, asfloat=0):
    x, y = x*1.0-self.tileHeight/2, y*1.0
    tx = (y - x/2)/self.tileHeight
    ty = (y + x/2)/self.tileHeight

    if not asfloat:
      return -floor(tx), floor(ty)
    else:
      return -tx, ty


  # gets the general isometric tile shape
  def getIsometricShape(self, Cx, Cy, offset=True):
    # create the iso tile shape
    if offset:
      tilePoints = [
        (self.offsetX + Cx+self.tileWidth/2, self.offsetY + Cy),
        (self.offsetX + Cx+self.tileWidth,   self.offsetY + Cy+self.tileHeight/2),
        (self.offsetX + Cx+self.tileWidth/2, self.offsetY + Cy+self.tileHeight),
        (self.offsetX + Cx,                  self.offsetY + Cy+self.tileHeight/2)
      ]
    else:
      tilePoints = [
        (Cx+self.tileWidth/2, Cy),
        (Cx+self.tileWidth,   Cy+self.tileHeight/2),
        (Cx+self.tileWidth/2, Cy+self.tileHeight),
        (Cx,                  Cy+self.tileHeight/2)
      ]
    return tilePoints


  # gets the place to blit an iso shape so it will align with the tile grid
  def getIsometricImagePosition(self, Cx, Cy):
    Tx = Cx + self.offsetX
    Ty = Cy + self.offsetY + self.tileHeight
    return Tx, Ty


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

      # also, load entities
      if tileStuffs.has_key("entitys"):
        loadEntitesFromMap(self, tileStuffs["entitys"])