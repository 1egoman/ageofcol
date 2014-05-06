import pygame
import common
import cmd
import pipe

from ai import ai
from structures import camp
from panel import morepanel
from pygame.locals import *
from inventory import drawInv
# import levelparser

class event(object):
  shift = False
  dodebug = False

  def newevent(self, event):
    currenttoolrun = False

    if event.type == pygame.QUIT:
      common.running = False

    # Run readkeys()
    elif event.type == pygame.USEREVENT+1:
      self.readkeys()

    elif event.type == pygame.USEREVENT+2:
      self.onTenthSecond()

    elif event.type == pygame.VIDEORESIZE:
      self.resize(event)
      # render
      common.g.render()

    # Inventory event handler
    elif common.activetool == "inventory":
      if event.type == pygame.KEYDOWN and event.key == 284:
        common.debug = not common.debug
        print "Debug:", common.debug
      else:
        common.din.event(event, self.shift)
      return

    # Run the events for a paused game
    elif common.paused:
      common.pausemenu.event(event)








    elif event.type == pygame.KEYDOWN:
      # print event.key
      if common.debug: print "KEYDOWN:", event.key

      # Press F1 to hide GUI
      if event.key == 282:
        common.hiddengui = not common.hiddengui


      # Press F3 To toggle debug mode
      if event.key == 284:
        common.debug = not common.debug
        print "Debug:", common.debug



      # Do Chatbox
      self.doChatbox(event)



      # Pauses Game
      if event.key == 27:
        common.paused = not common.paused
        print "Paused:", common.paused

      elif event.key == K_m:
        common.showminimap = not common.showminimap
        common.mmapy = common.mmaph+5

        # update minimap
        if event.key == K_u: common.g.minimap = None




      elif event.key >= 49 and event.key <= 57 and common.paused != True: # number keys
        common.seltool = event.key-49 # Change the selected tool

      elif event.key >= 257 and event.key <= 265 and common.paused != True: # number pad keys
        common.seltool = event.key-257 # Change the selected tool










    elif event.type == pygame.MOUSEBUTTONDOWN:
      mx, my = event.pos



      # Do chatbox
      if not common.cb.hide: 
        ret = common.cb.event(event)




      # Do the toolbar
      elif my > common.height-(common.tilewidth+5):

        # get the x value from the left of the toolbar
        toolbarside = (common.width-common.tilewidth*9)/2

        # Make sure we didn't select a nonvalid item on the toolbar
        if mx > toolbarside and mx < common.tilewidth*9+toolbarside:

          # assign the tool that was clicked on
          toolnum = (mx-toolbarside)/common.tilewidth
          if common.debug: print "Clicked Tool", toolnum

          # Run the tool
          self.runtool(toolnum)
          currenttoolrun = True




      # Also, do the more menu
      if common.morepanel == True:
        self.doMorePanel(event)
        return



      # left button clicked
      if event.button == 1 and common.paused != True:

        if common.debug: print "CLICK LEFTBUTTON"
        selected = self.getSelection(mx, my) # get selected mob
        
        # Cannot select a village while holding shift
        if selected and selected.mobtype == "village" and self.shift: selected=None




        # Main Selection Code
        # If a mob/village is selected (and it isn't dead)
        if selected and selected.health > 0:

          # turn off the tool so a tool doesn't work when it shouldn't
          common.activetool = None

          # Assign the mob to common.selected
          common.selected = selected

          # set the debug text accordingly
          mobowner = selected.owner
          if selected.owner == common.username: mobowner = "you"
          if selected.owner == "": mobowner = "everyone"
          common.selectedtext = str(type(common.selected))+" Selected at "+str(selected.x)+", "+str(selected.y)+", owned by "+mobowner+", health "+str(selected.health)+"/"+str(selected.maxhealth)

        # if we didn't click on something.....
        else:

          # Start looking at the tools
          # If our user has the move tool active...
          if common.activetool == "move" and common.selected and not currenttoolrun:
            if common.debug: print "move tool"


            # in debug mode move the mob/thing to your mouse pos
            if self.shift and common.debug:
              common.selected.x = mx-common.mapx
              common.selected.y = my-common.mapy
            else:
              # otherwise just set a heading for the mob/thing
              common.ai.setHeading(common.selected, mx-common.mapx, my-common.mapy)

            # deselect the tool
            common.activetool = None

          # If the user didn't click on anything, deselect the current mob/structure/thing selected
          if my < common.height-(common.tilewidth+5):
            common.selected = None
            common.selectedtwo = None
            common.selectedtext = "Nothing Selected"

      elif event.button == 3 and common.selected:
        self.doSecondarySelect(event)








    elif event.type == pygame.MOUSEMOTION:
      mx, my = event.pos

      # Change tool by hovering over with mouse
      if my > common.height-(common.tilewidth+5) and common.paused != True:

        # get toolbar x value (same as above)
        toolbarside = (common.width-common.tilewidth*9)/2

        # Again, make sure we have a valid tile
        if mx > toolbarside and mx < common.tilewidth*9+toolbarside:

          # 'darken' that tile
          common.seltool = (mx-toolbarside)/common.tilewidth





    # Reset the variable for the next go-around
    currenttoolrun = False


  def readkeys(self):
    if not common.cb.hide: return

    keystate = pygame.key.get_pressed()

    if common.paused != True:
      if keystate[K_RSHIFT] or keystate[K_LSHIFT]: 
        speed = common.maxmovespeed
        self.shift = True
      else:
        speed = common.movespeed
        self.shift = False
      if keystate[K_UP] | keystate[K_w]:
        common.mapy += speed
      elif keystate[K_DOWN] | keystate[K_s]:
        common.mapy -= speed
      elif keystate[K_LEFT] | keystate[K_a]:
        common.mapx += speed
      elif keystate[K_RIGHT] | keystate[K_d]:
        common.mapx -= speed


  def runtool(self, toolnum):

    # Make sure something is selected
    if not common.selected: 
      if common.debug: print "PLEASE SELECT A MOB!"
      return


    # Open more tools panel
    if toolnum == common.toolbarwidth-1:
      common.morepanel = not common.morepanel

    # Pipes
    elif toolnum == 2 and "structures" in str(type(common.selected)) and "structures" in str(type(common.selectedtwo)):
      if common.debug: print "Adding a new pipe..."
      if hasattr(common.selected, "inventory") and hasattr(common.selectedtwo, "inventory") and common.selected.inventory and common.selectedtwo.inventory:
        pipe.guipipe(common.selected, common.selectedtwo)
      elif common.debug:
        print "Both the startpoint and endpoint need to have an inventory!"


    # Inventory Tool
    elif toolnum == 1 and hasattr(common.selected, "inventory") and (common.selected.owner == common.username or common.selected.owner == "everyone"):
      # Set the tool to be active
      if common.debug: print "INVENTORY TOOL ACTIVE"
      common.activetool = "inventory"

      # Create inventory object
      if hasattr(common.selected, "inventory") and common.selected.inventory:
        # Create an inventory object to be drawn
        ix, iy = 0, 0
        common.din = drawInv(common.screen, common.selected.inventory, (ix,iy), (common.selected.inventory.c, common.selected.inventory.r), craftsize=common.selected.craftsize)
      else:
        # If the selected thing doesn't have an inventory inside, deselect the tool
        common.activetool = None


    # Deconstruct a structure
    elif toolnum == 0 and not "ai" in str(type(common.selected)):
      if ("structures" in str(type(common.selected)) or "sign" in str(type(common.selected))) and common.selected.owner == "everyone" or common.selected.owner == common.username:

        # Deconstruct a structure
        common.selected.deconstruct()
        common.selected = None # deselect it


    # Activate Move tool
    elif toolnum == 0 and common.selected.owner and common.selected.owner == common.username or common.selected.owner == "everyone":

      # Move Tool
      common.activetool = "move"
      self.tomove = common.selected
      if common.debug: print "MOVE TOOL ACTIVE"



    elif toolnum == 0 and common.selected and common.debug:
      print "MOVETOOL: DO NOT HAVE PERMISSION TO DO THIS!"




  def getSelection(self, x, y):
    # if common.activetool == "inventory": return
    s = common.ai.getMob(x, y)
    if not s:
      s = common.en.getEntity(x-common.mapx, y-common.mapy)
      if not s:
        s = common.cv.getStructure(x, y)
        return s
      else:
        return s
    else:
      return s





  def doChatbox(self, event):
    if not common.cb.hide and event.key == 27: common.cb.hide = True; common.cb.txt = ""

    elif not common.cb.hide: 
      ret = common.cb.event(event)
      if ret: 
        if common.debug: print "ISSUED COMMAND:", ret
        common.cb.items.insert(0,ret)
        common.cb.hide = True

        # Clear out notifications
        if ret == "/clean" or ret == "/clear" or ret == "/cls": cmd.posts = []; return
        
        # Run command
        cmd.run(ret)

    elif event.key == 32 or event.key == 116 or event.key == 47: # either press SPACE or t or /
      common.cb.hide = False



  def doMorePanel(self, event):
    mx, my = event.pos
    # get distance from the left in panel
    fl = (common.width-common.mp.panelw)/2
    bdr = 10

    if my >= common.mp.top and my <= common.mp.top+25 and mx >= fl and mx <= fl+common.mp.panelw:
      # Now, find what tab was clicked
      common.mp.activetab = ((mx-fl-bdr)/common.mp.tabw)
      if common.mp.activetab < 0: common.mp.activetab = 0
      if common.mp.activetab > len(common.mp.tabs)-1: common.mp.activetab = len(common.mp.tabs)-1

    elif my <= common.mp.top+common.mp.panelh and my >= common.mp.top+25 and mx >= fl and mx <= fl+common.mp.panelw:
      # TODO: slightly buggy
      yline = (my-common.mp.top)/(common.mp.tilewidth)
      xline = (mx-fl)/(common.mp.tilewidth+20)

      r = common.mp.clickedon(xline,yline)
      if r: 
        common.morepanel = False

    elif (my >= common.mp.top+common.mp.panelh or my <= common.mp.top+25 or mx <= fl or mx >= fl+common.mp.panelw) and my < common.height-common.tilewidth:
      common.morepanel = False


  def onTenthSecond(self):
    common.time += 0.1
    if common.debug: self.dodebug = True

  def doSecondarySelect(self, event):
    mx, my = event.pos
    selected = self.getSelection(mx, my) # get selected mob

    if selected:
      common.selectedtwo = selected
    else:
      common.selectedtwo = None

  def resize(self, event):
    # set width and height, then resize window
    common.width = event.w
    common.height = event.h
    common.screen = pygame.display.set_mode((common.width, common.height), RESIZABLE)
    common.mmapy = common.height-common.mmaph-5
    common.mmapx = 5
    if common.debug: print "RESIZED TO", common.width, common.height