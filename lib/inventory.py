import pygame
from entity import *
import common
import pipe

FURNACE = 1

items = {}
def addItemType(self, Iid, name, surface):
  if not surface: return

  # Add the item
  items[Iid] = (name, surface)



class playertotals(object):

  def __init__(self): self.contents = []

  def additem(self, Iid, amt):
    for c in xrange(0,amt):
      self.contents.append(Iid)

  def delitem(self, Iid, amt):
    for c in xrange(0,amt):
      self.contents.remove(Iid)



class inventory(object):

  # DRAWING SETTINGS
  # rows and columns
  r,c = 8,3

  # The distance the structure needs to be to another to move things there
  movedisance = 10

  def __init__(self): 
    self.contents = []
    self.floating = None
    self.cookitem = None


  # Add item to inventory
  def additem(self, item, count):
    # maxsize = self.r*self.c
    # size = len([list(f) for f in self.getContentsStacked()]+[[]][0])
    # if size > maxsize: return False
    if len(self.getContentsStacked())+int(count/common.en.stacksize[item]) > self.r*self.c: return False 

    for c in xrange(0, count):
      self.contents.append(item)
    return True



  # Remove item from inventory
  def delitem(self, item, count):
    for c in xrange(0, count):
      self.contents.remove(item)



  # Return list of items
  def getContents(self):
    existing = []

    for i in self.contents:
      item = [q for q in existing if q[0] == i]

      if len(item):
        item[0][1] += 1
      else:
        existing.append([i, 1])

    # Convert existing into a tuple
    return tuple([tuple(a) for a in existing])

  # Return list of items, stacked
  def getContentsStacked(self, m=[]):
    rst = []
    if m:
      c = self.getContents()+tuple(m)
    else:
      c = self.getContents()

    for i in list(c):
      stacksize = entity.stacksize[i[0]]
      if i[1] > stacksize:
        for _ in xrange(0, i[1]/stacksize):
          rst.append((i[0], stacksize))

        rst.append((i[0], (i[1]%stacksize)))
      else:
        rst.append(i)

    return tuple(rst)



  # Return amount of a stack in an inventory
  def has(self, Iid):
    itemnumber=0
    for c in self.contents:
      if c == Iid:
        itemnumber += 1
    return itemnumber

class drawInv(object):
  mx=0
  my=None
  csize=32


  class slot(object):
    def __init__(self, x, y):
      self.x = x
      self.y = y
      self.item = None
      self.color = (120,120,120)
      self.type = None
      # self.readonly = False
      self.onclick = None
      self.style = None

  def __init__(self, screen, inv, (x,y), (r,c), **kwargs):
    self.screen = screen
    self.x = x
    self.y = y
    self.r = r
    self.c = c
    self.inv = inv
    self.shift = False

    self.width = (c*self.csize+12+x)
    self.height = (r-1)*self.csize+12+y

    if kwargs.has_key("craftsize"):
      self.craftw = kwargs['craftsize']
    else:
      self.craftw = 2

    self.slots = []

    self.nh = self.generateCraftingGrid(self.craftw,self.craftw,0,self.height+50, centerx=True)
    if hasattr(self.inv, "hasoven") and self.inv.hasoven: self.generateOvenGrid(self.craftw,self.craftw,0,self.height+50+self.nh/2, centerx=True)



  def clearAllSlots(self):
    for s in self.slots:
      if s.item: 
        self.inv.additem(*s.item)








  # crafting grid

  def generateCraftingGrid(self, r, c, ox=0, oy=0, **kwargs):
    spacing=2

    if kwargs.has_key("centerx") and kwargs['centerx'] == True:
      ox = (self.width-((r*self.csize+(spacing*r))+ox))/2

    for j in xrange(0, r):
      for k in xrange(0, c):
        self.slots.append( self.slot( (j*self.csize+(spacing*j))+ox, (k*self.csize+(spacing*k))+oy) )
        self.slots[-1].type = "craft"

    self.slots.append( self.slot( (r*self.csize+(spacing*r))+ox, oy ) )
    self.slots[-1].color = (0, 180, 180)
    self.slots[-1].type = "craft"
    self.slots[-1].style = "dest"
    self.slots[-1].onclick = self.clearCrafting

    return (self.craftw*self.csize+(spacing*self.craftw))+oy

  def clearCrafting(self, slot):
    # if self.inv.floating:
    #   self.inv.floating = slot.item 
    #   slot.item = None
    #   return

    if slot.item:
      for g in [g for g in self.slots if g.type == "craft" and g != slot]: 
        if g.item and g.item[1] == 1:
          g.item = None
        elif g.item:
          g.item = (g.item[0], g.item[1]-1)
        else:
          g.item = None


  def checkCrafting(self):

    # check crafting, see if any recipies matched
    slots = [r.item for r in self.slots if r.type == "craft"]
    oslot = [r for r in self.slots if r.type == "craft" and r.style == "dest"]
    if len(slots) == (self.craftw**2)+1:
      
      nslots = []
      for t in slots:
        if t:
          nslots.append(t[0])
        else:
          nslots.append(None)


      for k,e in entity.craftingrecp.items():
        if e:
          notc = False
          if e[0] == self.craftw**2:

            for t in xrange(0, len(e[1])):
              if nslots[t] != e[1][t]:
                notc = True

            if not notc:
              # set item if recipe worked
              oslot[0].item = (k[0], k[1])
              return

            # get rid of the item if the recipe doesn't work
            oslot[0].item = None





# oven

  def generateOvenGrid(self, r, c, ox=0, oy=0, **kwargs):
    spacing=2

    if kwargs.has_key("centerx") and kwargs['centerx'] == True:
      ox = (self.width-((4*self.csize+(spacing*4))+ox))/2


    self.slots.append( self.slot( ox,oy ))
    self.slots[-1].type = "oven"
    self.slots[-1].style = "itemin"

    self.slots.append( self.slot( ox,oy+self.csize+spacing) )
    self.slots[-1].type = "oven"
    self.slots[-1].style = "fuelin"

    self.slots.append( self.slot( ((4*self.csize+(spacing*4))+ox),oy ) )
    self.slots[-1].color = (0, 180, 180)
    self.slots[-1].type = "oven"
    self.slots[-1].style = "dest" 


  def checkOven(self):
    steps = 10
    width = 100
    spacing=2

    itemin = [r for r in self.slots if r.type == "oven" and r.style == "itemin"]
    if len(itemin): itemin = itemin[0]

    fuelin = [r for r in self.slots if r.type == "oven" and r.style == "fuelin"]
    if len(fuelin): fuelin = fuelin[0]

    itemout = [r for r in self.slots if r.type == "oven" and r.style == "dest"]
    if len(itemout): itemout = itemout[0]


    # draw 'progress bar'
    if itemin:
      pygame.draw.rect(self.screen, (140,140,140), (itemin.x+self.csize+spacing,itemin.y,width,self.csize) )
      if self.inv.cookitem: 
        pygame.draw.rect(self.screen, (0,180,180), (itemin.x+self.csize+spacing,itemin.y,width/steps*self.inv.cookitem[3],self.csize) )


    # new item to cook
    if itemin.item and fuelin.item and not self.inv.cookitem and common.en.fuels.has_key( fuelin.item[0] ) and common.en.ovenrecp.has_key( itemin.item[0] ): 
      if common.debug: print "cooking..."
      self.inv.cookitem = [itemin.item, common.time, common.en.fuels[ fuelin.item[0] ], 0, itemin.item[0]]

      # subtract 1 fuel
      fuelin.item = (fuelin.item[0], fuelin.item[1]-1)
      if fuelin.item[1] <= 0: fuelin.item = None

    # when it is time to increment the progressbar...
    if self.inv.cookitem and common.time >= self.inv.cookitem[1]+(self.inv.cookitem[2]/steps):
      if common.debug: print "increment cookbar..."

      # items switched or removed in the slot
      if (itemin.item and self.inv.cookitem[4] != itemin.item[0]) or not itemin.item:
          if common.debug: print "SMELTING FAIL!"
          self.inv.cookitem = None
          return


      # add a step to var
      self.inv.cookitem[3] += 1
      # reset the clock
      self.inv.cookitem[1] = common.time+(self.inv.cookitem[2]/steps)

      # if done...
      if self.inv.cookitem[3] >= steps:
        if common.debug: print "DONE cooking..."

        # subtract 1 item
        itemin.item = (itemin.item[0], itemin.item[1]-1)
        if itemin.item[1] <= 0: itemin.item = None


        # add 1 item
        itm = entity.ovenrecp[ self.inv.cookitem[4] ]
        if itm and itemout.item and itm[0] == itemout.item[0]:
          itemout.item = (itemout.item[0], itemout.item[1]+itm[1])
        else:
          itemout.item = itm

        self.inv.cookitem = None










  def render(self, **kwargs):

    screen = self.screen
    x = self.x
    y = self.y
    r = self.r
    c = self.c
    inv = self.inv
    # Offset of things being hovered over to the mouse
    offset = (10,10)

    csize = self.csize

    cinv = inv.getContentsStacked()
    itemnum = 0

    if kwargs.has_key('bgcolor'):
      # BG Color
      pygame.draw.rect(screen, kwargs['bgcolor'], (x,y,self.width+6,common.height))

      # Delete area
      pygame.draw.rect(screen, kwargs['bgcolor'], (self.width+8,0,common.entitywidth,common.entitywidth*2))
      common.screen.blit(pygame.transform.scale(common.g.deletetool, (20,20)), (self.width+9, 5))

    if kwargs.has_key('font'):
      font = kwargs['font']
    else:
      font = pygame.font.SysFont("monospace", 12)

    if kwargs.has_key('textcolor'):
      txtcolor = kwargs['textcolor']
    else:
      txtcolor = (255,255,255)



    # pygame.draw.rect(common.screen, (150,150,150), (self.x+self.width+6, self.y+2, csize, 2+(csize*2) ))

    # draw cells
    for cy in xrange(y+2, self.height, csize+2):
      for cx in xrange(x+2, self.width, csize+2):

        # Add one to the item to be drawn
        itemnum += 1

        # Draw the cell bg
        pygame.draw.rect(screen, (120,120,120), (cx,cy,csize,csize))

        # Draw the item, if possible
        if len(cinv) >= itemnum: # if item exists....
          eitem = cinv[itemnum-1] # get its id

          # Draw it on the grid
          try:
            itemimg = entity.itemslocation[ entity.itemsbyid[ eitem[0] ] ]
            screen.blit(common.g.itemtiles, (cx+5,cy+5), (itemimg[0], itemimg[1], common.entitywidth, common.entitywidth))
          except KeyError:
            raise ValueError, "Please Define item id "+str(eitem[0])

          # Draw the amount of the item if is over 1
          if eitem[1] > 1:
            rndr = font.render(str(eitem[1]), True, txtcolor)
            screen.blit(rndr, (cx+2,cy+2))



    # draw the slots
    for s in self.slots:
      # draw slot bg
      pygame.draw.rect(screen, s.color, (s.x, s.y, csize, csize))

      # draw item in slot
      # print s.item
      if s.item:

        try:
          itemimg = entity.itemslocation[ entity.itemsbyid[ s.item[0] ] ]
          screen.blit(common.g.itemtiles, (s.x+5,s.y+5), (itemimg[0], itemimg[1], common.entitywidth, common.entitywidth))
        except KeyError:
          raise ValueError, "Please Define item id "+str(s.item[0])

        if s.item[1] > 1:
          rndr = font.render(str(s.item[1]), True, txtcolor)
          screen.blit(rndr, (s.x+2,s.y+2))




    self.checkCrafting()
    if hasattr(self.inv, "hasoven") and self.inv.hasoven: self.checkOven()



    # Draw whatever is attached to the mouse cursor
    if self.my == None or self.mx == None: return

    # Draw tooltip if hovering over an item
    itemx = (self.mx-self.x)/(csize+4)
    itemy = (self.my-self.y)/(csize+4)
    if self.my != None and len(cinv) >= (itemy*c)+itemx+1 and (itemy*c)+itemx+1 > 0: 
      if self.shift:
        itemname = entity.displayname[ cinv[ (itemy*c)+itemx ][0] ] + " #" + str(cinv[(itemy*c)+itemx][0])
      else:
        itemname = entity.displayname[ cinv[ (itemy*c)+itemx ][0] ]
      rndr = font.render(itemname, True, txtcolor)
      pygame.draw.rect(self.screen, (0,0,0), (self.mx+offset[0],self.my+offset[1],rndr.get_width()+4,rndr.get_height()+4))
      screen.blit(rndr, (self.mx+2+offset[0],self.my+2+offset[1]))

    # Draw floating item
    if self.inv.floating:
      try:
        itemimg = entity.itemslocation[ entity.itemsbyid[ self.inv.floating[0] ] ]
        screen.blit(common.g.itemtiles, (self.mx-(common.entitywidth/2),self.my-(common.entitywidth/2)), (itemimg[0], itemimg[1], common.entitywidth, common.entitywidth))
      except KeyError:
        raise ValueError, "Please Define item id "+str(itemnum)




  # Runs on an event
  def event(self, event, shift=False):
    self.shift = shift

    if event.type == pygame.MOUSEMOTION:
      self.mx, self.my = event.pos

    elif event.type == pygame.KEYDOWN:
      if event.key == 27: 
        common.activetool = None
        common.selected = None

    elif event.type == pygame.MOUSEBUTTONDOWN:
      self.mx, self.my = event.pos




      # deselect inventory tool
      if self.mx > self.c*(self.csize+4) and not self.inv.floating:
        self.inv.floating = None
        common.activetool = None
        self.clearAllSlots()




      # get active slot (clicked on)
      slots = [f for f in self.slots if self.mx >= f.x and self.my >= f.y and self.mx <= f.x+self.csize and self.my <= f.y+self.csize]
      if len(slots):
        slot = slots[0]

        # do click method
        if slot.onclick: slot.onclick(slot)
        
        # item in slot and slot is a destination slot
        if self.inv.floating and slot.item and slot.item[0] == self.inv.floating[0] and slot.style == "dest":
          self.inv.floating = (slot.item[0], slot.item[1]+self.inv.floating[1])
          slot.item = None


        # item in slot is same type that is being held
        elif self.inv.floating and slot.item and slot.item[0] == self.inv.floating[0]:
          slot.item = (slot.item[0], slot.item[1]+self.inv.floating[1])
          self.inv.floating = None


        # item is held that is different from what is in the slot already
        elif self.inv.floating: 
          a = slot.item
          slot.item = self.inv.floating
          self.inv.floating = a


        # pick up an item, slot has nothing in it 
        else:
          self.inv.floating = slot.item
          slot.item = None







      else:
        if event.button == 3:
          itemx = (self.mx-self.x)/(self.csize+4)
          itemy = (self.my-self.y)/(self.csize+4)
          # print itemx, itemy

          cinv = self.inv.getContentsStacked()
          amttominus = 0
          try:
            # If there is already an item floating...
            if self.inv.floating:
              # And if that item trying to be picked up is the same type floating
              if self.inv.floating[0] == cinv[(itemy*self.c)+itemx][0] and cinv[(itemy*self.c)+itemx][0] in self.inv.contents:
                # Join Them
                self.inv.floating = (self.inv.floating[0], self.inv.floating[1]+1)
                amttominus = 1

              else:
                # Drop the old item, and pick up the new one
                self.inv.additem(self.inv.floating[0], self.inv.floating[1])
                self.inv.floating = (cinv[(itemy*self.c)+itemx][0], cinv[(itemy*self.c)+itemx][1])
                amttominus = cinv[(itemy*self.c)+itemx][1]
            else:
              # Create a new floating item
              if shift:
                # Pick up the whole stack
                self.inv.floating = (cinv[(itemy*self.c)+itemx][0], cinv[(itemy*self.c)+itemx][1])
                amttominus = cinv[(itemy*self.c)+itemx][1]
              else:
                try:
                  # Pick up 1 item
                  self.inv.floating = (cinv[(itemy*self.c)+itemx][0], 1)
                  amttominus = 1
                except IndexError:
                  # There is no item in the slot we clicked, so return
                  return

          except AttributeError:
            return
          except IndexError:
            return

          if self.inv.has(self.inv.floating[0]) >= amttominus:
            self.inv.delitem(self.inv.floating[0], amttominus)
          else:
            self.inv.floating = None




        # PLACE ITEM
        if event.button == 1:
          itemx = (self.mx-self.x)/(self.csize+4)
          itemy = (self.my-self.y)/(self.csize+4)
          # print itemx, itemy

          cinv = self.inv.getContents()
          amttoplus = 0
          try:
            # If there is already an item floating...
            if self.inv.floating:
              # And if that item trying to be placed is the same type floating
              if self.inv.floating[0] == (itemy*self.c)+itemx in self.inv.contents:
                # Join Them
                self.inv.floating = (self.inv.floating[0], self.inv.floating[1]-1)
                amttoplus = 1
              else:

                # Copy item into another structures inventory because the mouse isn't in the inventory area
                if self.mx > self.width or self.my > self.r*(self.csize+4):
                  
                  # Do the delete button
                  if self.mx < self.width+self.csize+4 and self.my < self.x+self.csize*2: self.inv.floating = None


                  structure = common.cv.getStructure(self.mx, self.my)
                  if not structure: structure = common.ai.getMob(self.mx, self.my)

                  # mae sure the new structure can be moved to (pipe)
                  thepipe = pipe.getPipeAt(common.selected, structure, order=False)
                  if thepipe:

                    # Make sure the new structure has an inventory first and is owned by you or everyone
                    if hasattr(structure, 'inventory') and (structure.owner == common.username or structure.owner == "everyone"):

                      # loop through the items, and put them into the pipe
                      for ict in xrange(0, self.inv.floating[1]): 
                        thepipe.contents.append( (self.inv.floating[0], ict*4) )

                      self.inv.floating = None
                    elif common.debug:
                      print "Structure or mob isn't owned by you or doesn't have an inventory!"
                else:
                  # Drop the floating item into the current inventory
                  self.inv.additem(self.inv.floating[0], self.inv.floating[1])
                  self.inv.floating = None

          except AttributeError:
            return
          except IndexError:
            return

          if self.inv.floating and self.inv.has(self.inv.floating[0]) >= amttoplus:
            self.inv.additem(self.inv.floating[0], amttoplus)
          else:
            self.inv.floating = None