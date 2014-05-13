from ai import *
import inventory
import common

# def addItem(pname, Iid, itype, (ix, iy), dname=None):
#   entity.items[pname] = Iid
#   entity.itemsbyid[Iid] = pname
#   entity.itemslocation[pname] = (ix*common.entitywidth, iy*common.entitywidth)
#   entity.itemstype[pname] = itype
#   if dname:
#     entity.displayname[Iid] = dname
#   else:
#     entity.displayname[Iid] = pname

#   for x in entity.items.items(): entity.itemsbyid = dict(entity.itemsbyid.items() + [(x[1], x[0])])

#TODO: sort items and item info
#TODO: update textures to show change to using only one meat item

class entity(object):
  entitys = []
  items = {
  #'pigmeat': 20,
  #'cowmeat': 21, 
  'meat': 20,

  'jellybeanseed': 22, 
  'potatoseed': 23, 
  'watermelonseed': 24, 
  'wheatseed': 25, 

  'waterbucket': 19, 
  'rawwood': 12, 
  'refinedwood': 15, 
  'sapling': 10, 

  'stone': 30, 
  'coal': 31, 
  'ironore': 32, 
  'iron': 33, 
  'copperore': 34, 
  'copper': 35, 
  'goldore': 36, 
  'gold': 37
  }

  itemsbyid = {}
  for x in items.items(): itemsbyid = dict(itemsbyid.items() + [(x[1], x[0])])

  w = common.entitywidth
  itemslocation = {
  #'pigmeat': (0,w*3), 
  #'cowmeat': (w,w*3),
  'meat': (0,w*3),

  'jellybeanseed': (w*2,w*3), 
  'potatoseed': (w*3,w*3), 
  'watermelonseed': (w*4,w*3), 
  'wheatseed': (w*5,w*3), 

  'waterbucket': (0,w*2), 
  'rawwood': (0,w),
  'refinedwood': (w,w), 
  'sapling': (w,w*4), 
  'stone': (0, w*5), 
  'coal': (w, w*5), 
  'ironore': (0, w*6), 
  'iron': (w, w*6), 
  'copperore': (w*2, w*5), 
  'copper': (w*3, w*5), 
  'goldore': (w*2, w*6), 
  'gold': (w*3, w*6)
  }

  itemstype = {
  #'pigmeat': 'food', 
  #'cowmeat': 'food', 
  'meat': 'food',

  'jellybeanseed': 'food', 
  'potatoseed': 'food', 
  'watermelonseed': 'food', 
  'wheatseed': 'food', 

  'waterbucket': 'other', 
  'rawwood': 'wood',
  'refinedwood': 'wood', 
  'sapling': 'wood', 
  'stone': 'ore', 
  'coal': 'ore', 
  'ironore': 'ore', 
  'iron': 'ore',
  'copperore': 'ore', 
  'copper': 'ore',
  'goldore': 'ore', 
  'gold': 'ore'
  }

  displayname = {
  #20: 'Pork', 
  #21: 'Steak', 
  20: 'Meat',

  22: 'Jelly Bean Seed',
  23: 'Potato Seed',
  24: 'Watermelon Seed',
  25: 'Wheat Seed',

  19: 'Water', 
  12: 'Lumber', 
  15: 'Refined Lumber', 
  10: 'Sapling', 
  30: 'Stone', 
  31: 'Coal Nugget', 
  32: 'Iron Ore', 
  33: 'Iron Ingot',
  34: 'Copper Ore', 
  35: 'Copper Ingot',
  36: 'Gold Ore', 
  37: 'Gold Ingot'
  }

  stacksize = {
  20: 16, 
  #21: 16, 
  22: 16,
  23: 16,
  24: 16,
  25: 16,
  19: 1, 
  12: 32,
  15: 32,

  10: 32, 
  30: 32, 
  31: 32, 
  32: 16, 
  33: 32,
  34: 16, 
  35: 32,
  36: 16, 
  37: 32
  }

  craftingrecp = {
  (15, 4, 0): (4, [12,None,None,None]),
  (15, 4, 1): (9, [12]+[None]*8), 
  (15, 4, 2): (16, [12]+[None]*15), 
  (15, 4, 3): (25, [12]+[None]*24), 

  (15, 1, 1): (9, [30,30,None,30,30,None,None,None,None])

  }

  ovenrecp = {
  12: (31, 2),
  32: (33, 1),
  34: (35, 1),
  36: (37, 1)
  }

  fuels = {
  31: 2.0,
  12: 5.0
  }

  # inventory.addItem('', 1, '', (1, 1), '')

  # inventory.addItem('pigmeat', 20, 'food', (0,3), 'Pork')
  # inventory.addItem('cowmeat', 21, 'food', (1,3), 'Steak')

  # inventory.addItem('waterbucket', 19, 'other', (0,2), 'Water')

  # inventory.addItem('rawwood', 12, 'wood', (0,1), 'Lumber')
  # inventory.addItem('sapling', 10, 'wood', (1,4), 'Sapling')

  # inventory.addItem('coalore', 30, 'ore', (0,5), 'Coal Ore')
  # inventory.addItem('coal', 31, 'ore', (1,5), 'Coal Nugget')
  # inventory.addItem('ironore', 32, 'ore', (0,6), 'Iron Ore')
  # inventory.addItem('iron', 33, 'ore', (1,6), 'Iron Ingot')

  def getEntity(self, x, y):
    # Get an instance of an entity at x, y
    for c in self.entitys:
      # print c.x, c.y, c.w, c.h
      # print x < c.x+10+c.w, x > c.x-10-c.w, y < c.y+10+c.h, y > c.y-10-c.h
      if x < c.x+10+c.w and x > c.x-10-c.w and y < c.y+10+c.h and y > c.y-10-c.h:
        return c



def doCrafting(items):
  if items == [None, None, None, None, None, None, None, None]: return None
  print items
  if items[0] == (10, 1):
    return 12

  return None



class entityinstance(object):
  x = 0
  y = 0
  w = 0
  h = 0
  hostile=False # Wether the mob is hostile toword other mobs
  maxhealth = 20 # Maximum amount of health for the mob
  health = maxhealth # Mob starting health
  mobtype = "single" # Mob type. Pig, cow, etc... is single, while tribe, etc... is many or multiple
  type="entity"
  owner="" # Owner of the mob (can change position, etc)
  name=None # Name of the mob
  headx=0
  heady=0
  headfor=0
  speed=0
  super=None
  craftsize = 2

  # all __init__ does is add the mob to the instance class
  def __init__(self):
    entity.entitys.append(self)


class sign(entityinstance):
  w = 300
  h = 100
  message=""
  health,maxhealth=5,5

  def __init__(self, message):
    super(sign, self).__init__()
    self.message = message

  def deconstruct(self):
    entity.entitys.remove(self)

  def render(self):
    # Draw the sign
    common.screen.blit(self.sign, (common.mapx+ins.x,common.mapy+ins.y))

    # If the sign is selected...
    if ins == common.selected:

      # Draw a 'chatbox' with the sign contents inside
      pygame.draw.rect(common.screen, (222,184,135), (common.mapx+ins.x-(ins.w/2),common.mapy+ins.y-ins.h-10,ins.w,ins.h))
      tx, ty = common.mapx+ins.x+3, common.mapy+ins.y-10
      pygame.draw.polygon(common.screen, (222,184,135), [(tx,ty), (tx+3,ty+6), (tx+6,ty)])

      _,fh = self.font.size("a") # get the font height
      for c,l in enumerate(ins.message.split("\n")):
        # If the sign text gets too long, break from the loop
        if (fh*c+5) > ins.h-fh: break
        # Draw the text
        common.screen.blit( self.font.render(l, True, (0,0,0)), (3+common.mapx+ins.x-(ins.w/2), (common.mapy+ins.y-ins.h-7)+(c*fh+5)) )
