import random, math
import common
import inventory as inv
import economy
import math
from entity import entityinstance, entity
import structures

import pygame

class ai(object):
  mobs = [] # list of mobs by title ('pig', 'cow')
  mobins = [] # list of all mob instances
  # entitys = []

  def new(self, t, *args):
    s=",".join([str(o) for o in args])
    exec t+"("+s+")"

  def getMob(self, x, y):
    # Get an instance of a mob at x, y
    x = x - common.mapx
    y = y - common.mapy
    # print "one", x, y
    for c in self.mobins:
      # if c.mobtype == "multiple" or c.mobtype == "many":
      #   # print c.xy[0][0], c.xy[0][1]
      #   if x < c.xy[0][0]+15 and x > c.xy[0][0]-15 and y < c.xy[0][1]+15 and y > c.xy[0][1]-15:
      #     return c
      # else:
      if x < c.x+c.size and x > c.x-c.size and y < c.y+c.size and y > c.y-c.size:
        return c

  def getTileBelow(self, x, y):
    # get current tile under x, y
    tx = x/common.tilewidth
    ty = y/common.tilewidth
    try: 
      return common.g.tilemap[int(tx)][int(ty)]
    except IndexError:
      return None



  def setHeading(self, forwhat, mx, my):
    # cx and cy are the change in x and y respectivly between the specified x and y and the current x and y
    # hx and hy are the amount to move in 1 frame
    # ht is the distance to move, total

    #     (x, y)
    #      |\  
    #      | \   each \ represents 1 movement (1 frame)
    #   cy |  \  of (hx, hy)
    #      |   \
    #      |    \
    #      ------ (mx, my)
    #        cx

    x, y = forwhat.x, forwhat.y
    cx, cy = abs(x-mx), abs(y-my)
    hy = forwhat.runspeed
    hx = float((hy*cx)/cy)
    if hy != 0:
      ht = cy/hy
    else:
      ht=0
    # print cx, cy, hx, hy, ht
    print "X Change:", cx, "Y Change:", cy, "X CPF:", hx, "Y CPF:", hy, "Total Dist:", ht
    if my < y: hy,hx = -hy,-hx
    if mx > x and my < y: hy,hx = hy,-hx
    if mx < x and my > y: hy,hx = hy,-hx
    forwhat.headx = hx
    forwhat.heady = hy
    forwhat.headfor = ht
    forwhat.headingTimer = common.time
    # print forwhat.headx

class mob(entityinstance):
  """
  Mob Class: all mobs must extend this so they acctully work and dont cause funky errors.
  """
  # mob position
  x = 0
  y = 0
  # mob size
  sx = 0
  sy = 0
  attackdist=15 # Attack Distance
  hostile=False # Wether the mob is hostile toword other mobs
  maxhealth = 20 # Maximum amount of health for the mob
  health = maxhealth # Mob starting health
  # xy = [] # List of sub-mob members, used in tribe, etc...
  mobtype = "single" # Mob type. Pig, cow, etc... is single, while tribe, etc... is many or multiple
  owner="everyone" # Owner of the mob (can change position, etc)
  name=None # Name of the mob

  # Used for headings
  headx=0
  heady=0
  headfor=0

  # Speed of the mob
  speed=0.1
  runspeed=1
  type="mob"

  size=16

  # all __init__ does is add the mob to the instance class
  def __init__(self):
    ai.mobins.append(self)

    self.length = 0
    self.maxlength = 5
    self.angle = 0
    self.headingTimer = 0

  def doAnyHeadings(self):

    if self.headfor > 0:
      # print self.headingTimer, "\t\t\t", common.time
      if common.ai.getTileBelow(self.x+int(self.headx), self.y+int(self.heady)) in common.g.blockedtiles: 
        self.headfor = 0
        print 1
      if common.time >= self.headingTimer :#and random.randrange(0, 2) == 1:
        self.x += self.headx
        self.y += self.heady
        # cast the numbers back to ints
        self.x, self.y = int(self.x), int(self.y)
        self.prevcoords = self.x, self.y
        self.headfor -= 1



  def dealWithOthers(self):
    # This is where we deal with other mobs
    for m in ai.mobins:
      # if the mob isn't the current one.....
      if m != self:
        # Run the expression set above. This checks to see if there are any mobs within the attack distance, and if so....
        if self.x > m.x-self.attackdist and self.x < m.x+self.attackdist and self.y > m.y-self.attackdist and self.y < m.y+self.attackdist:
          return m # return it
    return None



  def draw(self):
    if common.username == self.owner or self.owner == "everyone":
      c = pygame.Surface((self.size+6,self.size+6), pygame.SRCALPHA)
      pygame.draw.circle(c, (0,0,0,20), (3+self.size/2, 3+self.size/2), 14)
      common.screen.blit(c, (common.mapx+self.x-3, common.mapy+self.y-3))

  
    common.screen.blit(self.image, (common.mapx+self.x, common.mapy+self.y))


  def moveMob(self, min=0, max=20):
    if self.maxlength == 0:
      self.angle = random.randrange(0, 360)
      self.maxlength = random.randrange(min, max)
      self.length = 0

    elif self.headfor == 0:
      self.x = int(self.length * math.cos(math.radians(self.angle)))+self.prevcoords[0]
      self.y = int(self.length * math.sin(math.radians(self.angle)))+self.prevcoords[1]
      self.length += self.speed

      if self.length >= self.maxlength:
        self.maxlength = 0
        self.prevcoords = self.x, self.y

    self.doAnyHeadings()


class unit(mob):
  """
  Unit Mob: This is the class that represents every Unit in the game.
  """
  size = 15
  movechance = 1500
  memberdist = common.tilewidth
  waterchance = 150
  attackdist=50
  mobtype = "single"
  hostile = True

  maxhealth = 100
  health = maxhealth
  formation=""
  owner="everyone"
  speed = 0.2
  villagehealrate = 100 # The higher the number, the less chance of giving health to villages
  super = None
  utype ="builder"
  stopped=False

  # The 'heads' (or peoples faces) to draw
  heads = []

  def __init__(self, t, x, y, m=None, s=None):
    super(unit, self).__init__()

    self.x = x
    self.y = y
    self.owner = t
    if m != None: self.members = args[3]
    if s != None: self.super = args[4]

    # Create the instance of the inventory and wallet for the unit
    self.inventory = inv.inventory()
    self.inventory.craftsize = 3
    
    self.wallet = economy.wallet()

    self.prevcoords = (x,y)

    # Add the members
    self.members = []
    self.members.append([0,0]) # this is the main member (always at 0,0 relative to everyone else)
    self.members.append([random.randrange(0, self.size-5),random.randrange(0, self.size-5),5,5,random.randrange(1, 10)])
    self.members.append([random.randrange(0, self.size-5),random.randrange(0, self.size-5),5,5,random.randrange(1, 10)])
    self.members.append([random.randrange(0, self.size-5),random.randrange(0, self.size-5),5,5,random.randrange(1, 10)])
    self.members.append([random.randrange(0, self.size-5),random.randrange(0, self.size-5),5,5,random.randrange(1, 10)])
    self.members.append([random.randrange(0, self.size-5),random.randrange(0, self.size-5),5,5,random.randrange(1, 10)])
    self.members.append([random.randrange(0, self.size-5),random.randrange(0, self.size-5),5,5,random.randrange(1, 10)])

    self.foresttimer = 0

  def update(self):
    if common.paused: return
    # print common.cv.getStructure(self.x/common.tilewidth+common.mapx, self.y/common.tilewidth+common.mapy)
    # Move on a heading
    # self.doAnyHeadings()

    # 'scramble' the random number generator
    random.jumpahead(20)

    # make self.x and y = the leaders position
    self.members[0][0] = self.x
    self.members[0][1] = self.y

    self.moveMob()
    self.x, self.y = int(self.x), int(self.y)


    mob = self.dealWithOthers()
    # See if the mob exists, and is owned by a different pesron than the mob attacking it
    if mob != None and (self.owner != mob.owner):
      # print mob
      # This checks to see if the target is hostile, and if so sets the mob to be hostile as well.
      if self.hostile: mob.hostile = True
      # If the correct int is generated and the unit isn't dead....
      if random.randrange(0, self.attackdist) == 1 and self.health > 0:
        # decrement the enemy's health
        mob.health -= 1
        # If the animal died, drop meat
        if mob.health == 0:
          if common.debug: print "Unit Killed a Mob."
          #Gives unit rspective amount of meat for the mob it killed
          if mob.type == "mob" and mob.__class__.__name__ != "unit":
            if mob.__class__.__name__ == "pig": amt = pig.meatamt
            elif mob.__class__.__name__ == "cow": amt = cow.meatamt
            elif mob.__class__.__name__ == "vulture": amt = vulture.meatamt
            elif mob.__class__.__name__ == "frog": amt = frog.meatamt
            else: print "Unknown Mob Type"
            self.inventory.additem(20,amt)
            self.wallet.amount += float(mob.maxhealth/10)

    # Healing
    elif mob == None and "village" in str(type(common.cv.getStructure(self.x/common.tilewidth, self.y/common.tilewidth))) and random.randrange(0, self.attackdist) == 1 and self.health < self.maxhealth and self.health > 0:
      self.health += 1
      # If in a village you own, double healing (increment twice)
      if self.super and (self.super.owner == self.owner or self.super.owner == "everyone"): self.health += 1





    # If there is water near, give the unit some water
    ifthereiswater = common.ai.getTileBelow(self.x+common.tilewidth,self.y) == "water"
    ifthereiswater = ifthereiswater or common.ai.getTileBelow(self.x-common.tilewidth,self.y) == "water"
    ifthereiswater = ifthereiswater or common.ai.getTileBelow(self.x,self.y+common.tilewidth) == "water"

    if ifthereiswater:
      # if common.debug: print "found water"
      if random.randrange(0, self.waterchance) == 1:
        # add water
        self.inventory.additem(19,1)



    # If the unit is on a forest for 10 sec give 2 wood
    if common.ai.getTileBelow(self.x,self.y) == "forest" and not self.foresttimer: self.foresttimer = common.time + 10.0
    if common.ai.getTileBelow(self.x,self.y) != "forest": self.foresttimer = 0.0

    if self.foresttimer and common.time >= self.foresttimer and common.ai.getTileBelow(self.x,self.y) == "forest":
      self.foresttimer = 0.0
      common.g.tilemap[self.x/common.tilewidth][self.y/common.tilewidth] = "grass"
      self.inventory.additem(12,2)




    # Deal with villages that are around...
    self.super = common.cv.getStructure(self.x+common.mapx, self.y+common.mapy)

    if self.super and (self.super.owner == self.owner or self.super.owner == "everyone"):
      # If the village needs to be healed, heal it.
      if self.utype.lower() == "builder" and random.randrange(0,self.villagehealrate) == 1 and self.super.health != self.super.maxhealth: 
        self.super.health += (len(self.members)/5) 

      # Empty inventory into village inventory, if you own the unit and village, and the village isn't a camp
      if (self.super.owner == self.owner or self.super.owner == "everyone" or self.owner == "everyone") and "camp" not in str(type(self.super)) and hasattr(self.super, "inventory"):
        
        # Get the type of structure that was walked over
        if type(self.super) == structures.village:
          # Empty inventory into village
          self.super.inventory.contents += self.inventory.contents
          self.inventory.contents = []


        elif type(self.super) == structures.woodyard or type(self.super) == structures.oremine:
          # Take inventory from a woodyard
          self.inventory.contents += self.super.inventory.contents
          self.super.inventory.contents = []

        if hasattr(self.super, "wallet"):
          # Also, transfer money into the village (if it has a wallet)
          self.super.wallet.amount += self.wallet.amount
          self.wallet.amount = 0.00

        if common.debug and self.inventory.contents: print "Emptyed the unit's inventory into the structure!"

      # When inside a village, units arn't hostile.
      self.hostile = False
    else:
      # Otherwise be hostile
      self.hostile = True




    # If the unit can move, move
    if self.stopped == False:
      for ct,m in enumerate(self.members):
        if ct == 0:
          rand = random.randrange(0, self.movechance)
          if rand == 1: self.x += self.speed
          if rand == 2: self.x -= self.speed
          if rand == 3: self.y += self.speed
          if rand == 4: self.y -= self.speed  
        else:
          rand = random.randrange(0, self.movechance)
          if rand == 1: m[0] += self.speed
          if rand == 2: m[0] -= self.speed
          if rand == 3: m[1] += self.speed
          if rand == 4: m[1] -= self.speed 
  
          # Stay within defined distance
          # if common.debug: print m[0] > self.memberdist or m[1] > self.memberdist or m[0] < -self.memberdist or m[1] < -self.memberdist
          if m[0] > self.memberdist: m[0] = self.memberdist
          if m[1] > self.memberdist: m[1] = self.memberdist
          if m[0] < -self.memberdist: m[0] = -self.memberdist
          if m[1] < -self.memberdist: m[1] = -self.memberdist
  
          # Stay in the map
          if m[0] < 0: m[0] = 0
          if m[1] < 0: m[1] = 0
          if m[0] > common.width: m[0] = 0
          if m[1] > common.width: m[1] = 0

      # Now, make sure the mobs x and y coords are inside the map, so you don't get flying units
      if self.x > common.mapw-self.size-1: self.x = common.mapw-self.size
      if self.y > common.maph-self.size-1: self.y = common.maph-self.size

      # Also, make sure the 'members' of the unit arn't in any of those blocked tiles
      if common.ai.getTileBelow(int(self.x+m[0]), int(self.y+m[1])) in common.g.blockedtiles:
        # If they are, just subtract speed instead of adding (or vice versa)
        if rand == 1: m[0] -= self.speed
        if rand == 2: m[0] += self.speed
        if rand == 3: m[1] -= self.speed
        if rand == 4: m[1] += self.speed 

    # Do some sanity checking
    if self.x < 0: self.x = 0
    if self.y < 0: self.y = 0
    if self.health < 0: self.health = 0



  def draw(self):
    ox, oy = self.members[0][0], self.members[0][1]
    # common.screen.blit(self.builderimage, (common.mapx+ox, common.mapy+oy-10))
    for c,m in enumerate(self.members):
      if c != 0:
        if m[0] < 0: m[0] == 0
        if m[1] < 0: m[1] == 0
        common.screen.blit(self.heads[0][m[4]], (common.mapx+ox+m[0], common.mapy+oy+m[1]))

    common.screen.blit(self.heads[0][0], (common.mapx+ox, common.mapy+oy))

    return math.sqrt(2*(self.memberdist**2))


class pig(mob):
  """
  Pig Mob: This is the class that represents every pig in the game.
  """
  size = 16
  health = 20
  movechance = 80
  hostile = False
  owner="everyone"
  speed = 0.1
  meatamt = 4

  def __init__(self, t="everyone", x=0, y=0):
    super(pig, self).__init__()

    self.x = x
    self.y = y
    self.owner = t

    self.maxlength = 5
    self.prevcoords = (x,y)

  def update(self):
    if common.paused: return
    if common.ai.getTileBelow(self.x, self.y) == "water" and random.randrange(0, (self.maxhealth*10)+1) == 0: self.health -= 1

    mob = self.dealWithOthers()
    if mob != None:
      if mob.hostile: self.hostile = True
      if random.randrange(0, self.attackdist) == 1 and self.health > 0 and self.hostile:
        mob.health -= 1
        if mob.health == 0:
          if common.debug: print "DROP: PIGMEAT"
          
    # Healing
    elif mob == None and random.randrange(0, 500) == 1 and self.health < self.maxhealth and self.health > 0:
      self.health += 1

    self.moveMob()

    # Now, make sure the mobs x and y coords are inside the map, so you don't get flying pigs
    if self.x > common.mapw-self.size-1:
      self.x = common.mapw-self.size
    if self.y > common.maph-self.size-1:
      self.y = common.maph-self.size
    # Do some sanity checking
    if self.x < 0:
      self.x = 0
    if self.y < 0:
      self.y = 0
    if self.health < 0:
      self.health = 0



class cow(mob):
  """
  Cow Mob: This is the class that represents every cow in the game.
  """
  size = 15
  health = 35
  maxhealth = health
  movechance = 80
  hostile = False
  owner="everyone"
  speed = 0.1
  meatamt = 5

  def __init__(self, t="everyone", x=0, y=0):
    super(cow, self).__init__()

    self.x = x
    self.y = y
    self.prevcoords = (x,y)


  def update(self):
    if common.paused: return
    if common.ai.getTileBelow(self.x, self.y) == "water" and random.randrange(0, (self.maxhealth*10)+1) == 0: self.health -= 1

    self.doAnyHeadings()
    mob = self.dealWithOthers()
    if mob != None:
      if mob.hostile: self.hostile = True
      if random.randrange(0, self.attackdist) == 1 and self.health > 0 and self.hostile:
        mob.health -= 1
        if mob.health == 0:
          if common.debug: print "DROP: COWMEAT"


    # Healing
    elif mob == None and random.randrange(0, 500) == 1 and self.health < self.maxhealth and self.health > 0:
      self.health += 1


    self.moveMob()

    # Now, make sure the mobs x and y coords are inside the map, so you don't get flying cows
    if self.x > common.mapw-self.size-1:
      self.x = common.mapw-self.size
    if self.y > common.maph-self.size-1:
      self.y = common.maph-self.size
    # Do some sanity checking
    if self.x < 0:
      self.x = 0
    if self.y < 0:
      self.y = 0
    if self.health < 0:
      self.health = 0

    # if self.getTile(self.x, self.y) != "grass" and self.getTile(self.x, self.y) != "sand":
    #   return False


class vulture(mob):
  """
  Bird Mob: This is the class that represents every vulture in the game.
  """
  size = 15
  health = 35
  maxhealth = health
  movechance = 80
  hostile = True
  owner="everyone"
  speed = 0.4
  meatamt = 3

  def __init__(self, t="everyone", x=0, y=0):
    super(vulture, self).__init__()

    self.x = x
    self.y = y
    self.prevcoords = (x,y)


  def update(self):
    if common.paused: return

    self.doAnyHeadings()
    mob = self.dealWithOthers()
    if mob != None:
      if mob.hostile: self.hostile = True
      if random.randrange(0, self.attackdist) == 1 and self.health > 0 and self.hostile:
        mob.health -= 1
        if mob.health == 0:
          if common.debug: print "DROP: VULTUREMEAT"


    # Healing
    elif mob == None and random.randrange(0, 500) == 1 and self.health < self.maxhealth and self.health > 0:
      self.health += 1


    self.moveMob(100, 150)

    # Now, make sure the mobs x and y coords are inside the map, so you don't get flying cows
    if self.x > common.mapw-self.size-1:
      self.x = common.mapw-self.size
    if self.y > common.maph-self.size-1:
      self.y = common.maph-self.size


    # Do some sanity checking
    if self.x < 0:
      self.x = 0
    if self.y < 0:
      self.y = 0
    if self.health < 0:
      self.health = 0

    # if self.getTile(self.x, self.y) != "grass" and self.getTile(self.x, self.y) != "sand":
    #   return False



class frog(mob):
  """
  Frog Mob: This is the class that represents every frog in the game.
  """
  size = 15
  health = 35
  maxhealth = health
  movechance = 80
  hostile = False
  owner="everyone"
  speed = 0.1
  meatamt = 1

  def __init__(self, t="everyone", x=0, y=0):
    super(frog, self).__init__()

    self.x = x
    self.y = y
    self.prevcoords = (x,y)


  def update(self):
    if common.paused: return
    if common.ai.getTileBelow(self.x, self.y) == "water" and random.randrange(0, (self.maxhealth*10)+1) == 0: self.health += 1

    self.doAnyHeadings()
    mob = self.dealWithOthers()
    if mob != None:
      if mob.hostile: self.hostile = True
      if random.randrange(0, self.attackdist) == 1 and self.health > 0 and self.hostile:
        mob.health -= 1
        if mob.health == 0:
          if common.debug: print "DROP: FROGMEAT"


    self.moveMob(0,5)

    # Now, make sure the mobs x and y coords are inside the map, so you don't get flying cows
    if self.x > common.mapw-self.size-1:
      self.x = common.mapw-self.size
    if self.y > common.maph-self.size-1:
      self.y = common.maph-self.size
    # Do some sanity checking
    if self.x < 0:
      self.x = 0
    if self.y < 0:
      self.y = 0
    if self.health < 0:
      self.health = 0