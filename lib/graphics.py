import common
import os
import levelparser
import random
import pygame
import datetime
import cmd
import settings
import pipe

from ai import *
from structures import *
from pygame.locals import *
from inventory import playertotals, drawInv
from panel import morepanel
from math import pi

import entity

class graphics(object):
  gridcolor = (180,180,180)
  #pi = 3.1415 # Converting degrees to radians

  def __init__(self):
    pygame.font.init()

    self.smallfont = pygame.font.SysFont("FreeMono, Monospace", 10)
    self.font = pygame.font.SysFont("FreeMono, Monospace", 16) 
    self.largefont = pygame.font.SysFont("FreeMono, Monospace", 25) 
    
    self.tilemap = []
    self.blockedtiles = ["mountainhigh"]
    self.debugimg = None

    self.minimap = None



  def render(self):
    common.screen.fill((100,100,100))
    self.setCursor(common.cursor)

    # draw the background if the cell has an ivalid type (black)
    pygame.draw.rect(common.screen, (0,0,0), (common.mapx, common.mapy, common.mapw, common.maph))

    if common.enablesky:
      for bgx in xrange(0, common.width, self.sky.get_width()):
        for bgy in xrange(0, common.height, self.sky.get_height()):
          common.screen.blit(self.sky, (bgx,bgy))

    # loop through the array of tiles
    # print common.mapw/common.tilewidth, common.maph/common.tilewidth
    for tx in xrange(0, common.mapw/common.tilewidth):
      for ty in xrange(0, common.maph/common.tilewidth):

        renderx = (tx+1)*common.tilewidth > -common.mapx and (tx+1)*common.tilewidth > -(common.mapx+common.width)
        rendery = (ty+1)*common.tilewidth > -common.mapy and (ty+1)*common.tilewidth > -(common.mapy+common.height)

        if renderx and rendery:
          # test the tiles, then draw them in the specified space
          try:
            if self.tilemap[tx][ty] == "grass" or self.tilemap[tx][ty][0] == "grass":
              # biome-specific
              if len(self.tilemap[tx][ty]) >= 2 and self.tilemap[tx][ty][1] == "tiaga":
                common.screen.blit(self.snow, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
              elif len(self.tilemap[tx][ty]) >= 2 and self.tilemap[tx][ty][1] == "swamp":
                common.screen.blit(self.moss, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
              else:
                common.screen.blit(self.grass, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
    

            elif self.tilemap[tx][ty] == "water" or self.tilemap[tx][ty][0] == "water":

              if len(self.tilemap[tx][ty]) >= 2 and self.tilemap[tx][ty][1] == "swamp":
                common.screen.blit(self.swampwater, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
              else:
                common.screen.blit(self.water, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
    
            elif self.tilemap[tx][ty] == "sand" or self.tilemap[tx][ty][0] == "sand":
              common.screen.blit(self.sand, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
    
            elif self.tilemap[tx][ty] == "stone" or self.tilemap[tx][ty][0] == "stone":
              common.screen.blit(self.stone, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))

            elif self.tilemap[tx][ty] == "forest" or self.tilemap[tx][ty][0] == "forest":
              if len(self.tilemap[tx][ty]) >= 2 and self.tilemap[tx][ty][1] == "tiaga":
                common.screen.blit(self.winterforest, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))
              else:
                common.screen.blit(self.forest, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))


            elif self.tilemap[tx][ty] == "mountainlow" or self.tilemap[tx][ty][0] == "mountainlow":
              common.screen.blit(self.lowhill, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))

            elif self.tilemap[tx][ty] == "mountainhigh" or self.tilemap[tx][ty][0] == "mountainhigh":
              common.screen.blit(self.highhill, (tx*common.tilewidth+common.mapx, ty*common.tilewidth+common.mapy))


          except Exception: pass



    # draw the grid on top of the tiles
    for gridx in xrange(0, common.mapw+1, common.tilewidth):
      pygame.draw.line(common.screen, self.gridcolor, (common.mapx+gridx, common.mapy), (common.mapx+gridx, common.maph+common.mapy))
    for gridy in xrange(0, common.maph+1, common.tilewidth):
      pygame.draw.line(common.screen, self.gridcolor, (common.mapx, common.mapy+gridy), (common.mapw+common.mapx, common.mapy+gridy))

    # Make sure selected animal isn't dead....
    if common.selected and common.selected.health < 0: common.selected = None


    # Render Structures
    self.renderStructures()

    # Render all entitys
    self.renderEntitys()


    # fertilize mobs (spawn new ones)
    # if len(common.ai.mobins) < 10:#common.minmobstofertilize:
    #   mx = random.randrange(0, w*tilewidth)
    #   my = random.randrange(0, h*tilewidth)
    #   t = random.randrange(0, 3)
    #   common.ai.mobins.append( pig(None, mx, my) )


    # draw mobs/ai stuff
    for ct,ins in enumerate(common.ai.mobins):
      if ins.__class__.__name__ == "pig":
        ins.image = self.pig

      elif ins.__class__.__name__ == "cow":
        ins.image = self.cow

      elif ins.__class__.__name__ == "unit":
        ins.image = self.guy
        ins.leaderimage = self.leader

      elif ins.__class__.__name__ == "vulture":
        ins.image = self.vulture

      elif ins.__class__.__name__ == "frog":
        ins.image = self.frog

      ins.update()
      # print ins.health
      if ins.mobtype.lower() == "single" and ins.health > 0:

        # Draw the actual 'Mob'
        dret = ins.draw()

        if dret == None: dret = ins.size

        # Draw selection region
        if ins == common.selected:
          pygame.draw.ellipse(common.screen, (255,0,0), (common.mapx+ins.x-(dret/2), common.mapy+ins.y-(dret/2), ins.image.get_width()+dret, ins.image.get_height()+dret), 1)
        elif ins == common.selectedtwo:
          pygame.draw.ellipse(common.screen, (0,255,0), (common.mapx+ins.x-(dret/2), common.mapy+ins.y-(dret/2), ins.image.get_width()+dret, ins.image.get_height()+dret), 1)

        # Draw Heath bar
        health = (25*ins.health)/ins.maxhealth
        pygame.draw.rect(common.screen, (120,0,0), (common.mapx+ins.x-5, common.mapy+ins.y-4, 25, 4))
        pygame.draw.rect(common.screen, (0,120,0), (common.mapx+ins.x-5, common.mapy+ins.y-4, health, 4))
      
        # if ins.__class__.__name__ == "unit":
        #   # Draw badge above the unit
        #   pygame.draw.circle(common.screen, (0,0,0), (common.mapx+ins.x, common.mapy+ins.y-50), common.tilewidth/2+4)
        #   pygame.draw.arc(common.screen, (255,0,0), (common.mapx+ins.x-32, common.mapy+ins.y-82,common.tilewidth,common.tilewidth), 0, (self.pi*(270)/180), common.tilewidth/2)
        #   pygame.draw.circle(common.screen, (100,100,100), (common.mapx+ins.x, common.mapy+ins.y-50), common.tilewidth/2-5)


      # elif ins.mobtype.lower() == "multiple" or ins.mobtype.lower() == "many" and ins.health != 0:
        # for members in ins.members:
          # insx = members[0]
          # insy = members[1]
          # common.screen.blit(ins.image, (common.mapx+insx, common.mapy+insy))

    # Render all the tribes
    # self.renderTribes()

    # Render inventory
    self.renderInventory()

    # draw minimap
    self.renderMinimap()


    # Put the correct totals in the infopanel
    foodtotal,woodtotal = 0,0
    for f in common.inventorytotal.contents:
      try: 
        if entity.entity.itemstypebyid[f] == "wood":
          woodtotal += 1
        if entity.entity.itemstypebyid[f] == "food":
          foodtotal += 1
      except KeyError: break

    common.ip.setText(0,0,"Wood: "+str(woodtotal))
    common.ip.setText(0,1,"Hi: "+str(0))
    common.ip.setText(0,2,"Hi: "+str(0))
    common.ip.setText(0,3,"Food: "+str(foodtotal))
    common.ip.setText(0,4,"Hi: "+str(0))
    common.ip.setText(1,0,"Hi: "+str(0))
    common.ip.setText(1,1,"Hi: "+str(0))
    common.ip.setText(1,2,"Hi: "+str(0))
    common.ip.setText(1,3,"Hi: "+str(0))
    common.ip.setText(1,4,"Hi: "+str(0))

    # Draw infopanel
    common.ip.render(common.width-common.ip.width-5, common.height-common.ip.height-5, self.font, self.infobar)


    # Draw Tool Bar
    self.renderToolbar()

    # Draw Chat bar
    cmd.renderPosts()
    common.cb.render(common.screen)



    # Debug Screen (press F3 in game)
    if common.debug:

      # get the biome at mouse pos
      mx, my = pygame.mouse.get_pos()

      try:
        tile = self.tilemap[((-common.mapx)+mx)/common.tilewidth][((-common.mapy)+my)/common.tilewidth]
      except IndexError:
        tile = None

      if len(tile) == 1: tile = (tile, None)


      self.debugimg = pygame.Surface((common.width, 100), flags=pygame.SRCALPHA)

      text = self.font.render("X:"+str(common.mapx)+" Y:"+str(common.mapy)+" B:"+str(tile[1])+" FPS:"+str(round(common.clock.get_fps(), 2)), True, (255,255,255))

      self.debugimg.blit(text, (10, 10))
      text = self.font.render(common.debugtext, True, (255,255,255))
      self.debugimg.blit(text, (10, 25))
      text = self.font.render(common.selectedtext, True, (255,255,255))
      self.debugimg.blit(text, (10, 40))

      # Draw time in corner
      now = datetime.datetime.now()
      text = self.font.render(now.strftime("%I:%M %p"), True, (255,255,255))
      common.screen.blit(text, (common.width-90, 10))


      common.screen.blit(self.debugimg, (0,0))
      del self.debugimg


    # Pause Screen (Press Esc in game)
    if common.paused:
      # draw shaded background
      common.screen.blit(pygame.transform.scale(self.dimtile, (common.width, common.height)).convert_alpha(), (0,0))
      common.pausemenu.render()
      # TODO: make buttons on pause screen


    # refresh pygame screen
    pygame.display.flip()

  def loadall(self):
    srcpath = os.path.join(common.rootdir, common.srclocation)
    # This is where all graphics are loaded into memory

    if not os.path.exists(srcpath): 
      common.srclocation = os.path.join("texturepacks", "default")
      srcpath = os.path.join(common.rootdir, common.srclocation)


    self.dimtile = pygame.Surface((common.tilewidth, common.tilewidth), flags=pygame.SRCALPHA)
    pygame.draw.rect(self.dimtile, (0,0,0,80), (0,0,common.tilewidth,common.tilewidth))

    self.button = pygame.Surface((300, 20))
    pygame.draw.rect(self.button, (0,0,0), (0,0,275,20))
    pygame.draw.rect(self.button, (150,140,130), (0,0,300,20))

    self.sky = pygame.image.load(os.path.join(srcpath, "sky.png")).convert()
    self.bgtiles = pygame.image.load(os.path.join(srcpath, "bgtiles.png")).convert()



    self.grass = pygame.Surface((common.tilewidth, common.tilewidth))
    self.grass.blit(self.bgtiles, (0,0), (0,0,common.tilewidth,common.tilewidth))


    self.snow = pygame.Surface((common.tilewidth, common.tilewidth))
    self.snow.blit(self.bgtiles, (0,0), (common.tilewidth*3,common.tilewidth,common.tilewidth,common.tilewidth))

    self.winterforest = pygame.Surface((common.tilewidth, common.tilewidth))
    self.winterforest.blit(self.bgtiles, (0,0), (common.tilewidth*4,common.tilewidth,common.tilewidth,common.tilewidth))


    self.moss = pygame.Surface((common.tilewidth, common.tilewidth))
    self.moss.blit(self.bgtiles, (0,0), (common.tilewidth*3,0,common.tilewidth,common.tilewidth))

    self.swampwater = pygame.Surface((common.tilewidth, common.tilewidth))
    self.swampwater.blit(self.bgtiles, (0,0), (common.tilewidth*4,0,common.tilewidth,common.tilewidth))



    self.water = pygame.Surface((common.tilewidth, common.tilewidth))
    # pygame.draw.rect(self.water, (0,50,200), (0,0,common.tilewidth,common.tilewidth))
    self.water.blit(self.bgtiles, (0,0), (common.tilewidth,0,common.tilewidth,common.tilewidth))

    self.sand = pygame.Surface((common.tilewidth, common.tilewidth))
    self.sand.blit(self.bgtiles, (0,0), (common.tilewidth*2,0,common.tilewidth,common.tilewidth))

    # TODO: MAKE STONE TEXTURE!!!
    self.stone = pygame.Surface((common.tilewidth, common.tilewidth))
    self.stone.blit(self.bgtiles, (0,0), (common.tilewidth*5,common.tilewidth,common.tilewidth,common.tilewidth))

    # TODO: MAKE MOUNTAIN TEXTURE!!!
    self.lowhill = pygame.Surface((common.tilewidth, common.tilewidth))
    self.lowhill.blit(self.bgtiles, (0,0), (common.tilewidth,common.tilewidth,common.tilewidth,common.tilewidth))

    # TODO: MAKE MOUNTAIN TEXTURE!!!
    self.highhill = pygame.Surface((common.tilewidth, common.tilewidth))
    self.highhill.blit(self.bgtiles, (0,0), (common.tilewidth*2,common.tilewidth,common.tilewidth,common.tilewidth))

    self.forest = pygame.Surface((common.tilewidth, common.tilewidth))
    self.forest.blit(self.bgtiles, (0,0), (0,common.tilewidth,common.tilewidth,common.tilewidth))

    # # COASTLINE TILES

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[0].blit(self.bgtiles, (0,0), (common.tilewidth*3+0, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[1].blit(self.bgtiles, (0,0), (common.tilewidth*4, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[2].blit(self.bgtiles, (0,0), (common.tilewidth*5, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[3].blit(self.bgtiles, (0,0), (common.tilewidth*6, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[4].blit(self.bgtiles, (0,0), (common.tilewidth*7, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[5].blit(self.bgtiles, (0,0), (common.tilewidth*8, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[6].blit(self.bgtiles, (0,0), (common.tilewidth*9, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[7].blit(self.bgtiles, (0,0), (common.tilewidth*10, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # self.coastline[8].blit(self.bgtiles, (0,0), (common.tilewidth*11, 0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # # self.coastline[9].blit(self.bgtiles, (0,0), (common.tilewidth*12, 0,common.tilewidth,common.tilewidth))
    # self.coastline[9].blit(self.bgtiles, (0,0), (common.tilewidth*2,0,common.tilewidth,common.tilewidth))


    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # # self.coastline[10].blit(self.bgtiles, (0,0), (common.tilewidth*13, 0,common.tilewidth,common.tilewidth))
    # self.coastline[10].blit(self.bgtiles, (0,0), (common.tilewidth*2,0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # # self.coastline[11].blit(self.bgtiles, (0,0), (common.tilewidth*14, 0,common.tilewidth,common.tilewidth))
    # self.coastline[11].blit(self.bgtiles, (0,0), (common.tilewidth*2,0,common.tilewidth,common.tilewidth))

    # self.coastline.append(pygame.Surface((common.tilewidth, common.tilewidth)))
    # # self.coastline[12].blit(self.bgtiles, (0,0), (common.tilewidth*15, 0,common.tilewidth,common.tilewidth))
    # self.coastline[12].blit(self.bgtiles, (0,0), (common.tilewidth*2,0,common.tilewidth,common.tilewidth))


    # END COASTLINE

    self.toolbar = pygame.Surface((common.tilewidth*9, common.tilewidth))
    pygame.draw.rect(self.toolbar, (200,200,200), (0,0,self.toolbar.get_width(),self.toolbar.get_height()))


    # mobs
    self.animimg = pygame.image.load(os.path.join(srcpath, "mobs", "mobs.png")).convert_alpha()

    self.pig = pygame.Surface((16,16), flags=pygame.SRCALPHA)
    self.pig.blit(self.animimg, (0,0), (0,0,16,16))

    self.cow = pygame.Surface((cow.size, cow.size), flags=pygame.SRCALPHA)
    self.cow.blit(self.animimg, (0,0), (16,0,16,16))

    self.vulture = pygame.Surface((vulture.size, vulture.size), flags=pygame.SRCALPHA)
    self.vulture.blit(self.animimg, (0,0), (32,0,16,16))

    self.frog = pygame.Surface((frog.size, frog.size), flags=pygame.SRCALPHA)
    self.frog.blit(self.animimg, (0,0), (48,0,16,16))

    self.guy = pygame.Surface((unit.size, unit.size), flags=pygame.SRCALPHA)
    pygame.draw.rect(self.guy, (180,175,160,200), (0,3,10,10))

    self.leader = pygame.Surface((unit.size, unit.size), flags=pygame.SRCALPHA)
    pygame.draw.rect(self.leader, (140,135,120,200), (0,3,10,10))

    self.sign = pygame.Surface((15,15)).convert_alpha()
    pygame.draw.rect(self.sign, (139,126,102), (0,0,15,15))
    pygame.draw.rect(self.sign, (210,180,140), (0,0,15,10))
    pygame.draw.line(self.sign, (139,126,102), (2,2), (12,2), 1)
    pygame.draw.line(self.sign, (139,126,102), (2,4), (12,4), 1)
    pygame.draw.line(self.sign, (139,126,102), (2,6), (12,6), 1)

    # self.builderimg = pygame.Surface((unit.size, unit.size), flags=pygame.SRCALPHA)
    # pygame.draw.rect(self.leader, (140,135,120,200), (0,3,10,10))


    # INFOPANEL IMAGES
    self.infobar = []

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[0], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[1], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[2], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[3], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[4], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[5], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[6], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[7], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[8], (150,150,107), (0,0,15,15))

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[9], (150,150,107), (0,0,15,15))

    # TOOLBAR IMAGES
    self.movetool = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "tools", "move.png")), (common.tilewidth-2, common.tilewidth-2)).convert_alpha()
    self.actiontool = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "tools", "action.png")), (common.tilewidth-2, common.tilewidth-2)).convert_alpha()
    self.inventorytool = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "tools", "inventory.png")), (common.tilewidth-2, common.tilewidth-2)).convert_alpha()
    self.deletetool = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "tools", "delete.png")), (common.tilewidth-2, common.tilewidth-2)).convert_alpha()
    self.constructortool = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "tools", "new.png")), (common.tilewidth-2, common.tilewidth-2)).convert_alpha()
    self.pipetool = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "tools", "pipe.png")), (common.tilewidth-2, common.tilewidth-2)).convert_alpha()

    # Houses
    civilization.buildingtextures = ["" for _ in xrange(0, 5)]
    civilization.buildingtextures[0] = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "house1.png")), (common.cv.housewidth, common.cv.housewidth)).convert_alpha()
    civilization.buildingtextures[1] = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "house2.png")), (common.cv.housewidth, common.cv.housewidth*2)).convert_alpha()
    civilization.buildingtextures[2] = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "tent.png")), (common.cv.tentwidth, common.cv.tentwidth)).convert_alpha()
    civilization.buildingtextures[3] = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "farm.png")), (int(common.cv.housewidth*1.5), int(common.cv.housewidth*1.5))).convert_alpha()
    civilization.buildingtextures[4] = pygame.transform.scale(common.cv.buildingtextures[2], (35,35))

    self.townhall = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "townhall.png")), (common.cv.townhallwidth, common.cv.townhallwidth)).convert_alpha()

    # Head Images (villages and units)
    heads = pygame.image.load(os.path.join(srcpath, "village", "people.png")).convert_alpha()
    civilization.heads = []
    for h in xrange(0, 10):
      civilization.heads.append(None)
      civilization.heads[h] = pygame.Surface((5,5))
      civilization.heads[h].blit(heads, (0,0), (h*5, 0, 5, 5))

    heads = pygame.image.load(os.path.join(srcpath, "mobs", "unitheads.png")).convert_alpha()
    for h in xrange(0, 10):
      unit.heads.append([])
      for i in xrange(0, 10):
        unit.heads[h].append("")
        unit.heads[h][i] = pygame.Surface((8,8), flags=pygame.SRCALPHA)
        unit.heads[h][i].blit(heads, (0,0), (i*8, 0, 8, 8))


    # woodyard
    civilization.woodyard = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "woodyard.png")), (common.tilewidth-12, common.tilewidth-12)).convert_alpha()
    civilization.woodyardold = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "woodyardold.png")), (common.tilewidth-12, common.tilewidth-12)).convert_alpha()

    # oremine
    civilization.oremine = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "mine.png")), (common.tilewidth-12, common.tilewidth-12)).convert_alpha()
    civilization.oremineold = pygame.transform.scale(pygame.image.load(os.path.join(srcpath, "village", "mineold.png")), (common.tilewidth-12, common.tilewidth-12)).convert_alpha()


    # Launcher Images
    common.logo = pygame.image.load(os.path.join(srcpath, "village", "townhall.png")).convert_alpha()

    self.itemtiles = pygame.image.load(os.path.join(srcpath, "items.png")).convert_alpha()
    self.constructortiles = pygame.image.load(os.path.join(srcpath, "constructors.png")).convert_alpha()

    # Unit badges
    # self.unitbadges = []

    self.infobar.append(pygame.Surface((15, 15)))
    pygame.draw.rect(self.infobar[0], (150,150,107), (0,0,15,15))

  def renderMinimap(self):
    if not common.showminimap: return
    if not common.cb.hide: return
    spacing = 300

    # generate the tile width, both horizontally or verically
    tilesizew = (common.width-spacing)/len(self.tilemap)
    tilesizeh = (common.height-spacing)/len(self.tilemap[0])

    # take the smaller of the two
    if tilesizew < tilesizeh:
      tilesize = int(round(tilesizew))
    else:
      tilesize = int(round(tilesizeh))


    # if the finished tilesize is bigger than 20, make it 20
    if tilesize > 20: tilesize = 20

    # generate the width, height, and x, y coords of the map
    width = len(self.tilemap)*tilesize
    height = len(self.tilemap[0])*tilesize
    mx = (common.width-width)/2
    my = (common.height-height)/2

    # If minimap doesn't exist, make it, then render it
    if not self.minimap: self.renderMinimapImg(width, height, tilesize)
    common.screen.blit(self.minimap, (mx,my))

    # draw location
    scale = (tilesize+0.0)/common.tilewidth
    pygame.draw.rect(common.screen, (255,0,0), (mx+(-common.mapx*scale), my+(-common.mapy*scale), int(common.width*scale), int(common.height*scale)), 1)


  def renderMinimapImg(self, width, height, tilesize):
    self.minimap = pygame.Surface((width, height))
    # draw the tiles
    for x in xrange(0, width, tilesize):
      for y in xrange(0, height, tilesize):
        
        tile = self.tilemap[x/tilesize][y/tilesize]
        biome = None

        if len(tile) != 1: 
          tile = self.tilemap[x/tilesize][y/tilesize][0]
          biome = self.tilemap[x/tilesize][y/tilesize][1]


        if biome == "swamp":
          color = (160,180,133)

        elif tile == "water":
          color = (20,10,180)

        elif (tile == "grass" or tile == "forest") and biome == "tiaga":
          color = (255,255,255)

        elif tile == "grass":
          color = (0,180,0)

        elif tile == "mountainlow":
          color = (80,120,80)

        elif tile == "mountainhigh":
          color = (102,51,0)

        elif tile == "sand":
          color = (220,180,130)

        elif tile == "forest":
          color = (0,120,0)

        else:
          color = (0,0,0)

        pygame.draw.rect(self.minimap, color, (x, y, tilesize, tilesize))




  def renderToolbar(self):
    if common.hiddengui or not common.selected: return
    # background: 
    common.screen.blit(self.toolbar, ( (common.width-self.toolbar.get_width())/2, common.height-self.toolbar.get_height()-5 ) )

    if common.selected:
      tbx = (common.width-self.toolbar.get_width())/2
      tby = common.height-self.toolbar.get_height()-5

      if "ai" in str(type(common.selected)): 
        common.screen.blit(self.movetool, (tbx+1,tby+1))

      if "structures" in str(type(common.selected)): 
        common.screen.blit(self.deletetool, (tbx+1, tby+1))
      # common.screen.blit(self.actiontool, (tbx+1+common.tilewidth,tby+1))
      if hasattr(common.selected, "inventory") and common.selected.inventory != None: 
        common.screen.blit(self.inventorytool, (tbx+1+common.tilewidth,tby+1))

      # For Constructor Menu (More Panel)
      common.screen.blit(self.constructortool, (tbx+1+(common.tilewidth*8), tby+1))

      if "structures" in str(type(common.selected)) and "structures" in str(type(common.selectedtwo)) and \
      hasattr(common.selected, "inventory") and hasattr(common.selectedtwo, "inventory") and common.selected.inventory and common.selectedtwo.inventory:
        if not pipe.getPipeAt(common.selected, common.selectedtwo):
          # Draw pipe
          common.screen.blit(self.pipetool, (tbx+1+(common.tilewidth*2),tby+1))
        else:
          # delete tool later?
          common.screen.blit(self.pipetool, (tbx+1+(common.tilewidth*2),tby+1))



    for barct in xrange(0, self.toolbar.get_width(), common.tilewidth):
      rndr = self.font.render(str(barct/common.tilewidth+1), True, (255,255,255))
      common.screen.blit(rndr, (((common.width-self.toolbar.get_width())/2)+barct+1, (common.height-common.tilewidth)-4))
    # Show tool selection with dimming of bar
    common.screen.blit(self.dimtile, ( (common.width-self.toolbar.get_width())/2+(common.seltool*common.tilewidth), common.height-self.toolbar.get_height()-5 ) )

    # Draw a additional panel if the user has selected to do so
    if common.morepanel: common.mp.render()

  def renderTribes(self):
      # DRAW TRIBES
      for inst in ai.tribes:
        # print inst.members[0]
        spritesurface = self.guy
        leadersurface = self.leader
        inst.update()
        for pos,members in enumerate(inst.members):
          insx = members[0]
          insy = members[1]
          # print pos, insx, insy
          if pos != 0:
            common.screen.blit(spritesurface, (common.mapx+insx, common.mapy+insy))

        common.screen.blit(leadersurface, (common.mapx+inst.members[0][0], common.mapy+inst.members[0][1]))

        health = (50*inst.health)/inst.maxhealth
        pygame.draw.rect(common.screen, (120,0,0), (common.mapx+inst.members[0][0]-25, common.mapy+inst.members[0][1]-10, 50, 5))
        pygame.draw.rect(common.screen, (0,120,0), (common.mapx+inst.members[0][0]-25, common.mapy+inst.members[0][1]-10, health, 5))

        # Draw selection region
        if inst == common.selected:
          # inst.formation="yline"
          # pygame.draw.rect(common.screen, (255,0,0), (common.mapx+inst.members[0][0]-8, common.mapy+inst.members[0][1]-8, spritesurface.get_width()+16, spritesurface.get_height()+16), 2)
          pinsx,pinsy,r=0,0,0
          for pos,members in enumerate(inst.members):
            insx = members[0]
            insy = members[1]
            if insx > pinsx or insy > pinsy:
              if insx > insy:
                # print inst.members[0][0]
                r = insx-(inst.members[0][0]-100)
              else:
                # print inst.members[0][1]
                r = insy-(inst.members[0][1]-100)
            # print r

            pinsx = insx
            pinsy = insy
          # r = 15
          pygame.draw.circle(common.screen, (255,0,0), (common.mapx+inst.members[0][0]+5, common.mapy+inst.members[0][1]+6), r/2, 1)

  def renderStructures(self):
    for v in common.cv.structures:
      if v.health > 0:
        v.render()

        if common.selected == v:
          pygame.draw.ellipse(common.screen, (255,0,0), (common.mapx+v.x-50, common.mapy+v.y-50, v.w+100, v.h+100), 1)

        elif common.selectedtwo == v:
          pygame.draw.ellipse(common.screen, (0,255,0), (common.mapx+v.x-50, common.mapy+v.y-50, v.w+100, v.h+100), 1)

  def setCursor(self, cursor):
    if cursor == "arrow" or cursor == None or cursor == "":
      cursorstring = (               #sized 24x24
      "XX                      ",
      "XXX                     ",
      "XXXX                    ",
      "XX.XX                   ",
      "XX..XX                  ",
      "XX...XX                 ",
      "XX....XX                ",
      "XX.....XX               ",
      "XX......XX              ",
      "XX.......XX             ",
      "XX........XX            ",
      "XX........XXX           ",
      "XX......XXXXX           ",
      "XX.XXX..XX              ",
      "XXXX XX..XX             ",
      "XX   XX..XX             ",
      "     XX..XX             ",
      "      XX..XX            ",
      "      XX..XX            ",
      "       XXXX             ",
      "       XX               ",
      "                        ",
      "                        ",
      "                        ")

    elif cursor == "hand":
      cursorstring = (               #sized 24x24
        "       XX               ", 
        "  XX  X..X  XX          ", 
        " X..X X..X X..X         ", 
        " X..X X..X X..X         ", 
        " X..X X..X X..X         ", 
        " X..X X..X X..X         ", 
        " X....X...X...X         ", 
        " X............X         ", 
        "  X...........X         ", 
        "    X.......X           ", 
        "     XXXXX              ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
        )
       
       

    datatuple, masktuple = pygame.cursors.compile( cursorstring, black='.', white='X', xor='o' )
    pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )


  def drawFromConfig(self):

    for vc in common.structures:

      if vc[9] == "village": 

        haddtexture = []
        for hct in vc[6]:
          # print ''.join(hct[-1])
          haddtexture += [hct[:-1]+ [common.cv.buildingtextures[int(hct[-1])]] ]
        s = village(vc[1], vc[2], vc[3], vc[4], vc[0], vc[5], haddtexture)
        s.owner = vc[10]

      elif vc[9] == "camp": 
        s = camp(vc[1], vc[2])
        s.owner = vc[10]

      elif vc[9] == "woodyard": 
        s = woodyard(vc[1], vc[2])
        s.owner = vc[10]

      elif vc[9] == "oremine": 
        s = oremine(vc[1], vc[2])
        s.owner = vc[10]

      else: 
        raise IndexError("Please Specify a structure type!")
        
      if len(common.cv.structures):
        common.cv.structures[-1].health = int(vc[7])
        common.cv.structures[-1].maxhealth = int(vc[8])
        common.cv.structures[-1].owner = vc[10]


  def renderEntitys(self):
    # Render all the entitys in ai.entitys
    for ct,ins in enumerate(common.en.entitys):
      # Render the entity
      ins.render()

  def renderInventory(self):
    if not common.selected: return

    if hasattr(common.selected, 'inventory') and common.selected.inventory != None and common.activetool == "inventory":
      # Render the inventory on the page

      # Render the inventory by the mob?
      # common.din.x = common.mapx+common.selected.x+3
      # common.din.y = common.mapy+common.selected.y+10

      common.din.render(bgcolor=(180,180,180))