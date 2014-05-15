import pygame
from pygame.locals import *
from math import *
import os

# constants
FACE_EAST = 0
FACE_WEST = 1

# load entities from a map file
def loadEntitesFromMap(iso, ent):
  # loop through...
  for e in ent:

    # get entity type
    exec "eType = %s" % e["type"]
    

    # create a new instance
    g = eType( iso, 0, 0, 0 )
    g.__dict__.update(e)


    # village specific stuff
    if type(g) == Village:
      cpy = e["buildingList"][:]
      g.buildingList = []

      # unpack all buildings
      for t in cpy:

        # get structure type
        if t.has_key("type"):
          exec "tType = g.%s" % t["type"]
        else:
          tType = g.Building

        # create it
        b = tType(g, 0, 0, 0)
        b.__dict__.update( t )
        g.buildingList.append(b)


    # add to stack
    iso.entityList.append(g)


""" Represents an entity in the game """
class Entity(object):

  # initialize
  def __init__(self, imap, x, y, w=1, h=1):

    # map the entity is part of
    self.isoMap = imap

    # entity x and y
    self.eX, self.eY = x, y

    # entity width and height
    self.eWidth, self.eHeight = w, h

    # health
    self.health = 1 # float from 0 to 1

    # owners
    self.owner = ["Player"]




  # render the entity
  def draw(self):

    # get tile position
    # tilePoints = self.isoMap.getIsometricShape( (self.eX)*self.isoMap.tileWidth, (self.eY-1)*self.isoMap.tileHeight )\
    Tx, Ty = self.isoMap.IsoToScreen(self.eX, self.eY)
    tilePoints = self.isoMap.getIsometricShape( Tx, Ty )

    # draw tile
    pygame.draw.polygon(self.isoMap.s, (255, 0, 0), tilePoints)












""" A Village is a basic civilization """
class Village(Entity):

  # color for shaded area under village
  SHADE_COLOR = (100, 100, 100, 127)




  """ This class represents a building """
  class Building(object):

    # initilize
    def __init__(self, p, x, y, facing=FACE_EAST):
      self.bX, self.bY = x, y
      self.parentVillage = p
      self.faceDirection = facing

      # contains the 2 surfaces for the opposite building sides
      self.buildingSurfaceEast = None
      self.buildingSurfaceWest = None


      self.loadImage()

    # load a buildings's image
    def loadImage(self, location="res"):
      path = os.path.join( os.path.abspath(location), "entitys", "building.png" )

      # get the surfaces
      self.buildingSurfaceEast = pygame.image.load(path).convert_alpha()
      self.buildingSurfaceWest = pygame.transform.flip(self.buildingSurfaceEast, 1, 0)



    def draw(self):
      # parse building position
      Sx, Sy = self.parentVillage.isoMap.IsoToScreen(self.parentVillage.eX + self.bX, self.parentVillage.eY + self.bY)
      Px, Py = self.parentVillage.isoMap.getIsometricImagePosition(Sx, Sy)
      Py -= 16 + self.buildingSurfaceEast.get_height()

      # draw it
      if self.faceDirection == FACE_WEST:
        self.parentVillage.isoMap.s.blit(self.buildingSurfaceWest, (Px, Py))
      else:
        self.parentVillage.isoMap.s.blit(self.buildingSurfaceEast, (Px, Py))




  """ This class represents a 'campfire' """
  class Fire(Building):

    # load fire's image
    def loadImage(self, location="res"):
      path = os.path.join( os.path.abspath(location), "entitys", "fire.png" )
      self.Fire = pygame.image.load(path).convert_alpha()

    def draw(self):
      # get positions
      Sx, Sy = self.parentVillage.isoMap.IsoToScreen(self.parentVillage.eX + self.bX, self.parentVillage.eY + self.bY)
      Px, Py = self.parentVillage.isoMap.getIsometricImagePosition(Sx, Sy)
      Py -= 16 + self.Fire.get_height()

      # draw it
      self.parentVillage.isoMap.s.blit(self.Fire, (Px, Py))






  # initialize
  def __init__(self, *args):
    super(Village, self).__init__(*args)

    # list of buildings within the village
    self.buildingList = []


    # create a shaded tile surface
    self.shadedTile = pygame.Surface((self.isoMap.tileWidth, self.isoMap.tileHeight), SRCALPHA)

    # draw the shape to it
    tilePoints = self.isoMap.getIsometricShape(0, 0, False) # False = no offset is applied to the points
    pygame.draw.polygon( self.shadedTile, self.SHADE_COLOR, tilePoints )

    # village population
    self.population = 0

    # load sample village
    # self.populateVillage()



  # draw it
  def draw(self):

    # draw shaded background
    for i in xrange(0, self.eWidth):
      for j in xrange(0, self.eHeight):
        
        # get positions
        Sx, Sy = self.isoMap.IsoToScreen(self.eX + i + 1, self.eY + j - 1)
        Px, Py = self.isoMap.getIsometricImagePosition(Sx, Sy)

        # draw it
        self.isoMap.s.blit(self.shadedTile, (Px, Py))


    # draw all buildings within village
    for b in self.buildingList:
      b.draw()


  # sample function to draw buildings in village
  def populateVillage(self):

    # positions of all the buildings
    buildingPositions = [
    (1.5, 1, FACE_EAST), 
    (0, 0, FACE_EAST), 
    (2, 2, FACE_WEST)
    ]

    # build the village
    for b in buildingPositions:
      b = self.Building(self, *b)
      self.buildingList.append(b)


  # format the object so it can be stored in json
  def formatForJSON(self):

    # start with all the attributes
    d = self.__dict__.copy()
    d["buildingList"] = d["buildingList"][:]

    # need to serialize buildingList
    for c,g in enumerate(d["buildingList"]):
      d["buildingList"][c] = g.__dict__.copy()

      # delete these keys
      del d["buildingList"][c]["buildingSurfaceEast"]
      del d["buildingList"][c]["buildingSurfaceWest"]
      del d["buildingList"][c]["parentVillage"]


    # delete some stuff
    del d["isoMap"]
    del d["shadedTile"]

    # return it
    return d