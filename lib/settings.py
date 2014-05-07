import pygame
import common
import os
#import yaml

class pausemenu(object):
  insettings = False
  bw = 500
  by = 150
  bx = (common.width-bw)/2

  def __init__(self):
    self.pevent = None
    self.settings = settings()

  def render(self):
    if self.insettings:
      self.settings.render()
    else:
      self.renderpause()



  def renderpause(self):
    self.bx = (common.width-self.bw)/2



    if self.pevent and self.pevent.type == pygame.MOUSEBUTTONDOWN:
      button = (self.pevent.pos[1]-self.by)/75
    else:
      button = -1


    if button == 0:
      pygame.draw.rect(common.screen, (150,150,150), (self.bx,0+self.by,self.bw,50))
    else:
      pygame.draw.rect(common.screen, (180,180,180), (self.bx,0+self.by,self.bw,50))
    rndr = common.g.largefont.render("Resume Game", True, (255,255,255))
    common.screen.blit(rndr, ((common.width-rndr.get_width())/2, 10+self.by))



    if button == 1:
      pygame.draw.rect(common.screen, (150,150,150), (self.bx,75+self.by,self.bw,50))
    else:
      pygame.draw.rect(common.screen, (180,180,180), (self.bx,75+self.by,self.bw,50))
    rndr = common.g.largefont.render("Settings", True, (255,255,255))
    common.screen.blit(rndr, ((common.width-rndr.get_width())/2, 85+self.by)) 
  


    if button == 2:
      pygame.draw.rect(common.screen, (150,150,150), (self.bx,150+self.by,self.bw,50))
    else:
      pygame.draw.rect(common.screen, (180,180,180), (self.bx,150+self.by,self.bw,50))
    rndr = common.g.largefont.render("Save Game", True, (255,255,255))
    common.screen.blit(rndr, ((common.width-rndr.get_width())/2, 160+self.by))



    if button == 3:
      pygame.draw.rect(common.screen, (150,150,150), (self.bx,225+self.by,self.bw,50))
    else:
      pygame.draw.rect(common.screen, (180,180,180), (self.bx,225+self.by,self.bw,50))
    rndr = common.g.largefont.render("Quit", True, (255,255,255))
    common.screen.blit(rndr, ((common.width-rndr.get_width())/2, 235+self.by))


  def event(self, event):

    if self.insettings: self.settings.event(event)

    self.pevent = event
    # Key handlers
    if event.type == pygame.KEYDOWN:
      if event.key == 27: 
        common.paused = False
        self.insettings = False
        print "Paused: False"

    elif event.type == pygame.MOUSEBUTTONUP:
      mx, my = event.pos
      if mx < self.bx or mx > self.bx+self.bw: return
      button = (my-self.by)/75
      
      # Resume Game
      if button == 0:
        common.paused = False
        print "Paused: False"

      elif button == 1:
        self.insettings = True

      elif button == 2:
        common.g.level.savelevel()
        common.paused = False
        print "Paused: False"

      # Quit
      elif button == 3:
        common.quitToLauncher = True
        common.paused = False
        common.cv.structures = []
        common.running = False
        self.minimap = None





class guiswitch(object):

  def __init__(self):
    self.state = False

  def togglestate(self):
    if self.state:
      self.state = False
    else:
      self.state = True

  def render(self, x, y):
    pygame.draw.rect(common.screen, (180,180,180), (x, y, 60, 25))

    if not self.state:
      pygame.draw.rect(common.screen, (10,180,180), (x, y, 30, 25))
    else:
      pygame.draw.rect(common.screen, (10,180,180), (x+30, y, 30, 25))



class settings(object):

  def __init__(self):
    self.rowone = [None for _ in xrange(0, 20)]
    self.rowtwo = [None for _ in xrange(0, 20)]
    self.rowthree = [None for _ in xrange(0, 20)]
    self.currenttexture = (0, "")

    self.rowone[0] = guiswitch()
    self.rowone[0].state = common.enablesky

    self.rowone[1] = guiswitch()

    self.currenttexture = [(ct,i) for ct,i in enumerate(list(os.listdir(os.path.join(common.rootdir, "texturepacks")))) if os.path.join("texturepacks", i) == common.srclocation][0]
    self.texture = self.currenttexture


  def event(self, event):

    if event.type == pygame.MOUSEBUTTONDOWN:
      mx, my = event.pos

      row = (my-20)/25
      print row

      if mx >= self.rowonex and mx <= self.rowonex+self.setwidth:
        self.doSetting(0, row)



  def doSetting(self, c, r):
    if c == 0:
      if r == 0:
        self.rowone[0].togglestate()
        common.enablesky = self.rowone[0].state
        self.writeConfigFile()

      elif r == 1:
        self.rowone[1].togglestate()

      elif r == 2:
        dirs = list(os.listdir(os.path.join(common.rootdir, "texturepacks")))
        # print len(dirs), self.currenttexture[0]
        if self.currenttexture[0] >= len(dirs): self.currenttexture[0] = 0
        self.currenttexture = [self.currenttexture[0]+1, dirs[self.currenttexture[0]]]
        common.srclocation = os.path.join("texturepacks", self.currenttexture[1])
        self.texture = self.currenttexture[1]
        common.g.loadall()

        self.writeConfigFile()



  def render(self):
    self.setwidth = 300
    self.rowonex = ((common.width-self.setwidth)/2)-(self.setwidth-20)
    self.rowtwox = ((common.width-self.setwidth)/2)
    self.rowthreex = ((common.width-self.setwidth)/2)-(self.setwidth+20)

    self.renderTextAt("Toggle Sky", self.rowonex+75, 22)
    self.rowone[0].render(self.rowonex,20) 

    self.renderTextAt("Night and Day", self.rowonex+75, 52)
    self.rowone[1].render(self.rowonex,50)

    common.screen.blit(common.g.button, (self.rowonex, 80))
    self.renderTextAt("Texture Pack:", self.rowonex+5, 82)
    if self.currenttexture: self.renderTextAt(self.currenttexture[1], self.rowonex+135, 82)

  def renderTextAt(self, t, x, y):
    rndr = common.g.font.render(t, True, (255,255,255))
    common.screen.blit(rndr, (x, y))

  def writeConfigFile(self):
    f = open(os.path.join(common.rootdir, "options.yml"), "w+")
    f.write("texturepack: "+str(self.texture[1])+"\n")
    f.write("sky: "+str(common.enablesky)+"\n")
    f.write("")
    f.close()
