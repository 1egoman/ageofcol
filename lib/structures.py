import common
import inventory as inv
import economy
import pygame
import random
import pipe

from entity import entityinstance, entity
from pygame.locals import *

class civilization(object):
  structures = []
  structuretypes = ["village", "camp", "woodyard", "oremine", "merchantshop", "villagehouse", "villagefarm", "villagebarrack"]
  housewidth = 30
  townhallwidth = 80
  tentwidth = 15
  buildingtextures = []

  # Add in village names here
  # TODO: put into a file on system
  nameone = ["Lema", "Mist", "North", "East", "South", "West", "Mil", "Barrow", "Iron", "Rock", "Harmon", "Center", "Cata", "Wilde", "Fox", "Way", "Dell", "Green", "Blue", "Land", "Merr", "Medow", "Gold", "By", "Winter", "Summer", "Spring", "Fall", "Mage", "Fun", "Lock", "Eri", "Clear", "Old", "Frey", "Sea", "Shell", "Haven", "Red", "Spen", "Syra", "Ron", "Stum", "Qwe", "Flat", "Tild"]
  nametwo = ["ville", "opilis", "town", "sis", "castle", "ilita", "ton", "port", "o", "uk", "burg", "borough"]

  def getStructure(self, x, y):
    x = x - common.mapx
    y = y - common.mapy
    # print "one", x, y
    for c in self.structures:
      # print c
      if x < c.x+c.w and x > c.x and y < c.y+c.h and y > c.y:
        return c

  def getTileBelow(self, x, y):
    # get current tile under x, y
    tx = x/common.tilewidth
    ty = y/common.tilewidth
    try: 
      return common.g.tilemap[tx][ty]
    except IndexError:
      return None

class building(entityinstance):
  bgcolor = (50,50,50)
  houseloc = []
  housect = 2
  constructable=False
  constructableifselected=False
  constructablematerialsneeded=[]
  moneytobepaid = 0
  unitplaceable=False
  mobtype="village"

  def __init__(self, *args, **kwargs):
    civilization.structures.append(self)
    self.deleting = False
    if common.cv.getTileBelow(self.x, self.y) == "water": self.delete()


  def render(self): 
    raise NotImplementedError('please define a .render() method!')

  def delete(self):
    p = pipe.getPipeAt(self, None)
    if p and p.contents: return

    if self in civilization.structures: 
      civilization.structures.remove(self)

    self.deleting = True

  def inViewPort(self):
    vpx = not (self.x+common.mapx < -200) and (self.x+common.mapx < common.width+200)
    vpy = not (self.y+common.mapy < -200) and (self.y+common.mapy < common.height+200)
    return vpy and vpx





class woodyard(building):
  w=common.tilewidth
  h=common.tilewidth
  constructable = True
  constructableifselected=False
  unitplaceable=True
  displayname="lumberyard"
  constructableifselected = "unit"
  constructablematerialsneeded = [entity.items['rawwood'], entity.items['rawwood']]

  woodfreq = 1000
  seedfreq = 250
  maxwood = 50

  craftsize=3


  def __init__(self, x, y):
    self.x = x*common.tilewidth
    self.y = y*common.tilewidth
    super(woodyard, self).__init__()

    self.inventory = inv.inventory()
    self.inventory.r = 8
    self.inventory.c = 5

    self.woodmade = 0
    if common.cv.getTileBelow(self.x, self.y) != "forest": self.delete()


  def render(self):
    if not self.inViewPort(): return

    if self.woodmade >= self.maxwood and self.inventory.contents == []: self.delete()
    # if self.woodmade >= self.maxwood or common.cv.getTileBelow(self.x, self.y) != "forest": self.delete()

      # Add the item if the woodyard has not reached max production
    if self.woodmade < self.maxwood:
      # Add item, and increment the wood count
      if random.randrange(0, self.woodfreq) == 0:
        self.inventory.additem(entity.items['rawwood'], 1)
        self.woodmade += 1

      if random.randrange(0, self.seedfreq) == 0:
        self.inventory.additem(entity.items['sapling'], 1)
        self.woodmade += 1

      wytexture = civilization.woodyard
    else:
      wytexture = civilization.woodyardold
      # Set tile below to be grass
      common.g.tilemap[self.x/common.tilewidth][self.y/common.tilewidth] = "grass"

    # Draw it
    villagebg = pygame.Surface((self.w,self.h))
    villagebg.set_alpha(50)
    villagebg.fill(self.bgcolor)
    common.screen.blit(villagebg, (common.mapx+self.x,common.mapy+self.y))

    common.screen.blit(wytexture, (common.mapx+self.x+6, common.mapy+self.y+6))

  def deconstruct(self): self.delete()





class oremine(building):
  w=common.tilewidth
  h=common.tilewidth
  constructable = True
  constructableifselected=False
  unitplaceable=True
  displayname="mine"
  constructableifselected = "unit"
  constructablematerialsneeded = [entity.items['rawwood'],entity.items['rawwood'],entity.items['rawwood'],entity.items['waterbucket']]

  ironfreq = 2000
  coalfreq = 1000
  stonefreq = 100
  copperfreq = 2000
  goldfreq = 3000
  maxitems = 100

  craftsize=3


  def __init__(self, x, y):
    self.x = x*common.tilewidth
    self.y = y*common.tilewidth
    super(oremine, self).__init__()

    self.inventory = inv.inventory()
    self.inventory.r = 8
    self.inventory.c = 5

    self.itemsmade = 0


  def render(self):
    if not self.inViewPort(): return

    if self.itemsmade >= self.maxitems and self.inventory.contents == []: self.delete()

    if self.itemsmade < self.maxitems:
      # Add item, and increment the wood count

      if random.randrange(0, self.stonefreq) == 0:
        self.inventory.additem(entity.items['stone'], 1)
        self.itemsmade += 1

      if random.randrange(0, self.coalfreq) == 0:
        self.inventory.additem(entity.items['coal'], 1)
        self.itemsmade += 1

      if random.randrange(0, self.ironfreq) == 0:
        self.inventory.additem(entity.items['ironore'], 1)
        self.itemsmade += 1

      if random.randrange(0, self.copperfreq) == 0:
        self.inventory.additem(entity.items['copperore'], 1)
        self.itemsmade += 1

      if random.randrange(0, self.goldfreq) == 0:
        self.inventory.additem(entity.items['goldore'], 1)
        self.itemsmade += 1

      omtexture = civilization.oremine
    else:
      omtexture = civilization.oremineold

    # Draw it
    villagebg = pygame.Surface((self.w,self.h))
    villagebg.set_alpha(50)
    villagebg.fill(self.bgcolor)
    common.screen.blit(villagebg, (common.mapx+self.x,common.mapy+self.y))

    common.screen.blit(omtexture, (common.mapx+self.x+6, common.mapy+self.y+6))

  def deconstruct(self): self.delete()



class villagehouse(building):
  constructable = True
  constructableifselected = "village"
  displayname="Village House"
  constructablematerialsneeded = [entity.items['rawwood'], entity.items['rawwood'], entity.items['rawwood'], entity.items['stone']]
  moneytobepaid = 50


class villagefarm(building):
  constructable = True
  constructableifselected = "village"
  displayname="Village Farm"
  constructablematerialsneeded = [entity.items['rawwood'], entity.items['rawwood'], entity.items['stone'], entity.items['waterbucket']]
  moneytobepaid = 50


class villagebarrack(building):
  constructable = True
  constructableifselected = "village"
  displayname="Village Barracks"
  constructablematerialsneeded = []
  moneytobepaid = 0



class merchantshop(building):
  # Area to trade materials for money or money for materials
  w=common.tilewidth
  h=common.tilewidth
  # constructable = True
  constructableifselected=False
  unitplaceable=True
  displayname="merchantshop"
  constructableifselected = "unit"
  constructablematerialsneeded = [entity.items['iron'], entity.items['rawwood']]

  woodfreq = 1000
  seedfreq = 250
  maxwood = 50
  craftsize=3

  def __init__(self, x, y):
    super(merchantshop, self).__init__()
    self.x = x*common.tilewidth
    self.y = y*common.tilewidth

    self.inventory = inv.inventory()
    self.inventory.r = 8
    self.inventory.c = 5

    self.woodmade = 0


  def render(self):
    if not self.inViewPort(): return

    if self.woodmade >= self.maxwood and self.inventory.contents == []: self.delete()
    # if self.woodmade >= self.maxwood or common.cv.getTileBelow(self.x, self.y) != "forest": self.delete()

      # Add the item if the woodyard has not reached max production
    if self.woodmade < self.maxwood:
      # Add item, and increment the wood count
      if random.randrange(0, self.woodfreq) == 0:
        self.inventory.additem(entity.items['rawwood'], 1)
        self.woodmade += 1

      if random.randrange(0, self.seedfreq) == 0:
        self.inventory.additem(entity.items['sapling'], 1)
        self.woodmade += 1

      wytexture = civilization.woodyard
    else:
      wytexture = civilization.woodyardold
      # Set tile below to be grass
      common.g.tilemap[self.x/common.tilewidth][self.y/common.tilewidth] = "grass"

    # Draw it
    villagebg = pygame.Surface((self.w,self.h))
    villagebg.set_alpha(50)
    villagebg.fill(self.bgcolor)
    common.screen.blit(villagebg, (common.mapx+self.x,common.mapy+self.y))

    common.screen.blit(wytexture, (common.mapx+self.x+6, common.mapy+self.y+6))

  def deconstruct(self): self.delete()






class village(building):
  bgcolor = (50,50,50)
  houseloc = []
  housect = 2
  housewidth = 30
  health = 250
  maxhealth = health
  mobtype = "village"
  hostile = False
  type="village"
  craftsize=4

  constructable = True
  constructableifselected = "unit"
  displayname="Village"
  constructablematerialsneeded = [entity.items['rawwood']]*15 + [entity.items['stone']]*10 + [entity.items['waterbucket']]*5
  moneytobepaid = 0


  def __init__(self, x, y, w=2, h=2, name=None, pop=5, hct=None):

    # print hct
    # hct=None
    # hct=None
    self.x = x*common.tilewidth
    self.y = y*common.tilewidth
    self.w = w*common.tilewidth
    self.h = h*common.tilewidth
    self.housect = 1
    self.population = pop
    super(village, self).__init__()

    self.inventory = inv.inventory()
    self.inventory.r = 8
    self.inventory.c = 8
    self.inventory.hasoven=True

    self.wallet = economy.wallet()
    self.wallet.capacity = 250.00

    self.inhabitants = []
    self.producefarm = 0.0
    self.producebarracks = 0.0
    self.refinetimer = 0.0
    self.orerefinetime = 2.0

    # Generate Village Name
    if not name:
      self.name = civilization.nameone[random.randrange(0, len(civilization.nameone))]+civilization.nametwo[random.randrange(0, len(civilization.nametwo))]
    else:
      self.name = name
    # Create house locations
    if hct:
      self.houseloc = hct
      self.housect = len(hct)
    else:
      for h in xrange(0, self.housect):
        hx = random.randrange(0, self.w-self.housewidth)
        hy = random.randrange(0, self.h-self.housewidth)
        self.houseloc.append([hx, hy, common.cv.buildingtextures[0]])

  def render(self):
    if not self.inViewPort(): return

    # Change population
    self.population = len([f for f in self.houseloc if f[2] == common.cv.buildingtextures[0]])*5

    # update inhabitants
    if (self.population/2) != len(self.inhabitants):
      for _ in xrange(0, (self.population/2)-len(self.inhabitants)):
        self.inhabitants.append([random.randrange(0, self.w), random.randrange(0, self.h), civilization.heads[random.randrange(0, len(civilization.heads))]])




    # update farm production
    farms = [f for f in enumerate(self.houseloc) if f[1][2] == common.cv.buildingtextures[3] ]
    if farms and not self.producefarm: self.producefarm = common.time + 10.0
    if farms and self.producefarm and common.time >= self.producefarm:
      self.producefarm = 0.0
      fgen = random.randrange(0, 3)
      if fgen == 0:
        self.inventory.additem(entity.items['jellybeanseed'], 1)
      elif fgen == 1:
        self.inventory.additem(entity.items['potatoseed'], 1)
      elif fgen == 2:
        self.inventory.additem(entity.items['wheatseed'], 1)
      elif fgen == 3:
        self.inventory.additem(entity.items['watermelonseed'], 1)


    # make barracks work
    barracks = [f for f in enumerate(self.houseloc) if f[1][2] == common.cv.buildingtextures[4] ]
    if barracks and not self.producebarracks: self.producebarracks = common.time + (5.0/len(barracks))
    if farms and self.producebarracks and common.time >= self.producebarracks:
      self.producebarracks = 0.0
      
      print "producebarracks"
      common.ai.new("unit", '"'+self.owner+'"', self.x, self.y)



    # Draw village background
    villagebg = pygame.Surface((self.w,self.h))
    villagebg.set_alpha(50)
    villagebg.fill(self.bgcolor)
    common.screen.blit(villagebg, (common.mapx+self.x,common.mapy+self.y))




    # If the village has ore in it, slowly refine it...
    # refine = [(c,g) for c,g in enumerate(self.inventory.contents) if entity.itemstype[entity.itemsbyid[g]] == 'ore' ]
    # if refine:

    #   if not self.refinetimer: self.refinetimer = common.time + self.orerefinetime + 0.0
    #   if self.refinetimer and common.time >= self.refinetimer:

    #     self.refinetimer = 0.0
    #     refine = [(c,g) for c,g in enumerate(self.inventory.contents) if entity.itemsbyid[g][-3:] == 'ore' ]
    #     if refine:
    #       itemname = entity.itemsbyid[ refine[0][1] ][:-3]
    #       self.inventory.contents[ refine[0][0] ] = entity.items[ itemname ] 




    # Loop through all the houses and draw them in the village
    for h in self.houseloc:
      # print h
      if h[2]:
        common.screen.blit(h[2], (common.mapx+self.x+h[0], common.mapy+self.y+h[1]))




    # loop through the villagers, and draw them
    for villager in self.inhabitants:
      if not common.paused:
        # Move it
        gen = random.randrange(0, 100)
        if gen == 1: villager[0] += 1
        if gen == 2: villager[0] -= 1
        if gen == 3: villager[1] += 1
        if gen == 4: villager[1] -= 1

        # Give money for 'work' the villager does (10 cents every 5 sec or so)
        if gen == 5: economy.pay(self.wallet, 0.10)

        if villager[0] < 0: villager[0] = 0
        if villager[1] < 0: villager[1] = 0
        if villager[0] > self.w: villager[0] = self.w
        if villager[1] > self.h: villager[1] = self.h

      # Draw it
      common.screen.blit(villager[2], (common.mapx+self.x+villager[0], common.mapy+self.y+villager[1]))




    # Find the center, and draw the town hall there
    if self.w/common.tilewidth > 1 or self.h/common.tilewidth > 1:
      common.screen.blit(common.g.townhall, ((common.mapx+self.x+self.w/2)-civilization.townhallwidth/2, (common.mapy+self.y+self.h/2)-civilization.townhallwidth/2))

  def deconstruct(self): self.delete()

class camp(building):
  inventory = None
  wallet = None
  lumberneeded = 10
  onewhoplaced = None
  maxhealth = 50
  health = maxhealth
  constructable = True
  constructableifselected="unit"
  unitplaceable=True

  constructablematerialsneeded=[entity.items['rawwood'] for _ in xrange(0,10)]

  def __init__(self, x, y, super=None):
    # why doesn't super work here?
    building.__init__(self)

    self.x = x*common.tilewidth
    self.y = y*common.tilewidth
    self.w = common.tilewidth
    self.h = common.tilewidth

    self.housect = 10
    self.houseloc.append([5, 4, common.cv.buildingtextures[2]])
    self.houseloc.append([5, 18, common.cv.buildingtextures[2]])
    self.houseloc.append([5, 32, common.cv.buildingtextures[2]])
    self.houseloc.append([5, 46, common.cv.buildingtextures[2]])

    self.houseloc.append([45, 4, common.cv.buildingtextures[2]])
    self.houseloc.append([45, 18, common.cv.buildingtextures[2]])
    self.houseloc.append([45, 32, common.cv.buildingtextures[2]])
    self.houseloc.append([45, 46, common.cv.buildingtextures[2]])

    self.houseloc.append([25, 4, common.cv.buildingtextures[2]])
    self.houseloc.append([25, 18, common.cv.buildingtextures[2]])
    self.houseloc.append([25, 32, common.cv.buildingtextures[2]])
    self.houseloc.append([25, 46, common.cv.buildingtextures[2]])

    # self.constructablematerialsneeded=[entity.items['rawwood'] for _ in xrange(0,10)]


  def render(self):
    if not self.inViewPort(): return

    # Draw village background
    villagebg = pygame.Surface((self.w,self.h))
    villagebg.set_alpha(50)
    villagebg.fill(self.bgcolor)
    common.screen.blit(villagebg, (common.mapx+self.x,common.mapy+self.y))

    # Loop through all the tents
    for h in self.houseloc: common.screen.blit(h[2], (common.mapx+self.x+h[0], common.mapy+self.y+h[1]))

  def deconstruct(self):
    if self.onewhoplaced:
      self.onewhoplaced.inventory.additem(entity.items['rawwood'],self.lumberneeded)
    civilization.structures.remove(self)