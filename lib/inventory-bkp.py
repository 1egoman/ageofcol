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
    self.craftsize = self.r



  # Add item to inventory
  def additem(self, item, count):
    # maxsize = self.r*self.c
    # size = len([list(f) for f in self.getContentsStacked()]+[[]][0])
    # if size > maxsize: return False

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

  craftingscroll = 0

  def __init__(self, screen, inv, (x,y), (r,c), **kwargs):
    self.screen = screen
    self.x = x
    self.y = y
    self.r = r
    self.c = c
    self.inv = inv
    self.shift = False

    if kwargs.has_key('craftingsize'):
      self.inv.craftsize = kwargs['craftsize']
    else:
      self.inv.craftsize = self.inv.r

    self.craftinglist = [None for _ in xrange(0, self.inv.craftsize)]
    self.craftingret = None

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
    self.width = (c*csize+12+x)
    self.height = (r-1)*csize+12+y

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






    # Draw crafting list
    if self.craftinglist != None:
      itemnum = 0
      starting = common.height-(20+self.csize)



      # Destination cell
      pygame.draw.rect(screen, (0,120,120), (self.x+2, starting-self.csize-2, csize, csize))
      if self.craftingret:
        # print self.craftingret

        try:
          itemimg = entity.itemslocation[ entity.itemsbyid[ self.craftingret ] ]
          screen.blit(common.g.itemtiles, (self.x+8, starting-self.csize+4), (itemimg[0], itemimg[1], common.entitywidth, common.entitywidth))
        except KeyError:
          raise ValueError, "Please Define item id "+str(eitem[0])

        # Draw the amount of the item if is over 1
        # if eitem[1] > 1:
          # rndr = font.render(str(self.craftingret[1]), True, txtcolor)
          # screen.blit(rndr, (self.x+2,starting-self.csize+4))



      # Input Cells
      for cx in xrange(y+2, self.width, csize+2):
        # Add one to the item to be drawn
        itemnum += 1

        # Draw the cell bg
        pygame.draw.rect(screen, (120,120,120), (self.x+cx, starting, csize, csize))

        # Draw it on the grid
        if len(self.craftinglist) >= itemnum and self.craftinglist[itemnum-1]:
          try:
            itemimg = entity.itemslocation[ entity.itemsbyid[ self.craftinglist[(itemnum-1)][0] ] ]
            screen.blit(common.g.itemtiles, (self.x+cx+5, starting+5), (itemimg[0], itemimg[1], common.entitywidth, common.entitywidth))
          except KeyError:
            raise ValueError, "Please Define item id "+str(self.craftinglist[itemnum-1][0])

          # Draw the amount of the item if is over 1
          if self.craftinglist[itemnum-1][1] > 1:
            rndr = font.render(str(self.craftinglist[(itemnum-1)][1]), True, txtcolor)
            screen.blit(rndr, (self.x+cx+5,starting+5))












    # Draw whatever is attached to the mouse cursor
    if self.my == None or self.mx == None: return

    # Draw tooltip if hovering over an item
    itemx = (self.mx-self.x)/(csize+4)
    itemy = (self.my-self.y)/(csize+4)
    if self.my != None and len(cinv) >= (itemy*c)+itemx+1 and (itemy*c)+itemx+1 > 0: 
      if self.shift:
        itemname = entity.displayname[ cinv[ (itemy*c)+itemx ][0] ] + " (" + str(cinv[(itemy*c)+itemx][0]) + ")"
      else:
        itemname = entity.displayname[ cinv[ (itemy*c)+itemx ][0] ]
      rndr = font.render(itemname, True, txtcolor)
      pygame.draw.rect(self.screen, (0,0,0), (self.mx+offset[0],self.my+offset[1],rndr.get_width()+4,rndr.get_height()+4))
      screen.blit(rndr, (self.mx+2+offset[0],self.my+2+offset[1]))

    # Draw floating item
    if self.inv.floating:
      try:
        itemimg = entity.itemslocation[ entity.itemsbyid[ self.inv.floating[0] ] ]
        screen.blit(common.g.itemtiles, (self.mx,self.my), (itemimg[0], itemimg[1], common.entitywidth, common.entitywidth))
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

      # Drop Into crafting
      if self.my > self.height-(20+self.csize) and self.inv.floating and event.button == 1 and self.mx <= self.width:
        cell = (self.mx)/(self.csize+4)

        # if the cell isn't filled
        if len(self.craftinglist) > cell or self.craftinglist[cell] != None: return

        # if self.craftinglist[cell][1] >= 1:
        # self.craftinglist[cell] = (self.inv.floating[0], self.craftinglist[cell][1]+self.inv.floating[1])
        # else:
        self.craftinglist[cell] = self.inv.floating

        print cell, self.craftinglist[cell]

        self.inv.floating = None
        self.craftingret = doCrafting(self.craftinglist)


      elif self.my > common.height-(20+self.csize) and not self.inv.floating and event.button == 3:
        cell = (self.mx)/(self.csize+4)
        self.inv.floating = self.craftinglist[cell]
        self.craftinglist[cell] = None

        self.craftingret = doCrafting(self.craftinglist)

      elif self.my < common.height-(20+self.csize) and self.mx <= self.csize+2 and not self.inv.floating and event.button == 3 and self.craftingret:
        self.inv.floating = (self.craftingret, 1)
        self.craftingret = None
        self.craftinglist = [None for _ in self.craftinglist]

      # End Drop Into Crafting




      if self.mx > self.c*(self.csize+4) and not self.inv.floating:
        self.inv.floating = None
        common.activetool = None


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