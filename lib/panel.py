import pygame
from pygame.locals import *
import common
from entity import *
from structures import *
from ai import *
import pipe

class morepanel(object):
  activetab = 0
  panelw = 500
  panelh = 400
  tabs = ["Buildings", "Village", "Pipes"]
  tabw = 100
  tabspace = 10
  top=100
  constructables = []
  tilewidth = 100
  border = 10
  bttiles = 10
  columns = 4

  locations = [
  {'camp': (0,0), 'woodyard': (0, tilewidth), 'oremine': (0,tilewidth*2), 'village': (tilewidth,0)}, 
  {'villagehouse': (0,tilewidth*3), 'villagefarm': (tilewidth,tilewidth)}, 
  'pipes']

  todraw = []
  matlist = []

  def render(self):
    if not hasattr(common.selected, 'inventory'): return
    # Draw background
    pygame.draw.rect(common.screen, (80,80,80), ((common.width-self.panelw)/2, self.top, self.panelw, self.panelh))

    # Draw tabs accross the top of the screen
    for c,t in enumerate(self.tabs):
      if not c == self.activetab:
        color = (150,150,150)
      else:
        color = (180,180,180)

      if type(self.locations[c]) == dict:
        # Draw tab + text
        pygame.draw.rect(common.screen, color, (((common.width-self.panelw)/2+10)+((self.tabspace+self.tabw)*c), self.top+5, self.tabw, 25))   
        txt = common.g.font.render(t, True, (0,0,0))
        common.screen.blit(txt, (((common.width-self.panelw)/2+10)+((self.tabspace+self.tabw)*c)+5, self.top+5))


    # Draw tab 'usable space'
    pygame.draw.rect(common.screen, (180,180,180), (((common.width-self.panelw)/2)+10, self.top+25, self.panelw-20, self.panelh-35))

    # get distance from the left in panel
    fl = (common.width-common.mp.panelw)/2

    if self.locations[self.activetab] == "pipes" and pipe.getPipeAt(common.selected):
      self.renderPipes()
      return

    # We have the construct tab selected, so things that can be made are put here.
    # define some variables
    todraw = [] 
    # print village.constructable
    for c in civilization.structuretypes:
      # get wether the structure is constructable or not...
      exec "constructable = "+c+".constructable"
      exec "constructableis = "+c+".constructableifselected"
      # If the structure is constructable
      if constructable == True:
        if constructableis:
          # Put in a list to be drawn
          if common.selected and constructableis in str(type(common.selected)) and type(self.locations[self.activetab]) == dict and self.locations[self.activetab].has_key(c): todraw += [c]
        else:
          # Put in a list to be drawn
          if self.locations[self.activetab].has_key(c): todraw += [c]
          # print "b"

    for c,d in enumerate(todraw):
      tx = fl+self.border+10+(c*(self.tilewidth+self.bttiles))
      ty = self.top+40

      self.todraw = todraw

      # Draw the tile
      pygame.draw.rect(common.screen, (150,150,150), (tx-2, ty-2,self.tilewidth+4,self.tilewidth+4))
      common.screen.blit(common.g.constructortiles, (tx,ty), (self.locations[self.activetab][d][0], self.locations[self.activetab][d][1],self.tilewidth,self.tilewidth))

      # If the user doesn't have the correct materials to make it, 'gray' it out
      exec "materials = "+d+".constructablematerialsneeded"
      exec "p = "+d+".moneytobepaid"
      x = [common.selected.inventory.has(f) >= materials.count(f) for f in materials]
      # print x

      if hasattr(common.selected, "wallet") and common.selected.wallet.amount >= p:
        money = True
      elif not hasattr(common.selected, "wallet"):
        money = True
      else:
        money = False

      if common.selected and hasattr(common.selected, 'inventory') and 0 in x and money:
        tilebg = pygame.Surface((100,100))
        tilebg.set_alpha(60)
        tilebg.fill((0,0,0))
        common.screen.blit(tilebg, (tx,ty))

        # Draw what you must 'spend' to get it
        # exec "materials = "+d+".constructablematerialsneeded"
        # if materials:

          # Get the number of each occerance of each item
          # matList = []
          # cmaterials = ""
          # for m in materials:
            # if (m,materials.count(m)) not in matList:
              # matList += [(m,materials.count(m))]
              # cmaterials += str(materials.count(m))+" "+entity.displayname[m]

          # self.matlist = matList
          # for c,mt in enumerate(matList):
            # txt = common.g.smallfont.render(cmaterials, True, (0,0,0))
            # common.screen.blit(txt, (tx+2+(c*common.g.smallfont.size(str(mt[1]))[0]), ty+2))

  def clickedon(self, y, x):
    for col,t in enumerate(self.todraw):
      row = col/self.columns

      if row == x and col == y:
        # print type(common.selected)
        if "ai" in str(type(common.selected)) or "structures" in str(type(common.selected)):
          if "village" not in t:
            exec "i = "+t+"("+str(common.selected.x/common.tilewidth)+", "+str(common.selected.y/common.tilewidth)+")"
            # print "i = "+t+"("+str(common.selected.x/common.tilewidth)+", "+str(common.selected.y/common.tilewidth)+")"
            i.owner = common.selected.owner
            if hasattr(i, "onewhoplaced"): i.onewhoplaced = common.selected

            # If the unit is placeable and commmon.selected isnt a unit, dont place...
            if hasattr(i, "unitplaceable") and i.unitplaceable == True and "unit" not in str(type(common.selected)): 
              civilization.structures.remove(i)
              return

            if hasattr(i, "villageplaceable") and i.villageplaceable == True and "structures" not in str(type(common.selected)): 
              civilization.structures.remove(i)
              return

          # money to pay
          exec "p = "+t+".moneytobepaid"
          if not economy.pay(common.selected.wallet, -p): return

          # Delete the materials
          doesnothavemat = False
          exec "mat = "+t+".constructablematerialsneeded"
          for a in mat:
            if not common.selected.inventory.has(a): 
              if "village" not in t:
                civilization.structures.remove(i)
              else:
                doesnothavemat = True
                break
              return
            else:
              common.selected.inventory.delitem(a, 1)

          # Add house
          if "villagehouse" in t and not doesnothavemat:
            hx, hy = self.generateHousePosition(common.selected)
            common.selected.houseloc.append([hx,hy,common.cv.buildingtextures[0]])


          if "villagefarm" in t and not doesnothavemat:
            hx, hy = self.generateHousePosition(common.selected)
            common.selected.houseloc.append([hx,hy,common.cv.buildingtextures[3]])

          if "villagebarrack" in t and not doesnothavemat:
            hx, hy = self.generateHousePosition(common.selected)
            common.selected.houseloc.append([hx, hy, common.cv.buildingtextures[4] ])

          common.morepanel = False
          self.matlist = []
        break
  
  def renderPipes(self):
    pass

  def generateHousePosition(self, selected):
    bad = False
    while bad == False:
      x = random.randrange(0, selected.w-common.cv.housewidth)
      y = random.randrange(0, selected.h-common.cv.housewidth)

      for h in selected.houseloc:
        if x < h[0]+100 and x > h[0]-100 or y < h[1]+100 and y > h[1]-100:
          bad = True
        else:
          bad = False
        # print x < h[0]+100, x > h[0]-100, y < h[1]+100, y > h[1]-100, bad

    return x, y