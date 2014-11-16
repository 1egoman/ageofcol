import pygame
from pygame.locals import *

import isomap, entity
from minimap import Minimap

class Game(object):

  # cursor strings
  hand_str = [
    "     ..         ",
    "    .xx.        ",
    "    .xx.        ",
    "    .xx.        ",
    "    .xx.....    ",
    "    .xx.xx.x..  ",
    " .. .xx.xx.x.   ",
    ".xx..xxxxxxxxx. ",
    ".xxx.xxxxxxxxx. ",
    " .xx.xx.x.x.xx. ",
    "  .xxxx.x.x.xx. ",
    "  .xxxx.x.x.x.  ",
    "   .xxx.x.x.x.  ",
    "    .xxxxxxx.   ",
    "     .xxxx.x.   ",
    "     ..... ..   "
  ]


  grabber_str = [
    "                ",
    "                ",
    "                ",
    "                ",
    "     .......    ",
    "    .xx.xx.x..  ",
    " .. .xx.xx.x.   ",
    ".xx..xxxxxxxxx. ",
    ".xxx.xxxxxxxxx. ",
    " .xx.xx.x.x.xx. ",
    "  .xxxx.x.x.xx. ",
    "  .xxxx.x.x.x.  ",
    "   .xxx.x.x.x.  ",
    "    .xxxxxxx.   ",
    "     .xxxx.x.   ",
    "     ..... ..   "
  ]


  def __init__(self):
    # init pygame
    pygame.init()

    # create surface
    self.s = pygame.display.set_mode((800, 600), RESIZABLE)

    # compile cursors
    self.cursorHand = pygame.cursors.compile(self.hand_str, 'x', '.', "o")
    self.cursorGrabber = pygame.cursors.compile(self.grabber_str, 'x', '.', "o")
    self.currentCursor = self.cursorHand



    # create the map
    self.iso = isomap.isoMap(self.s, 8, 8)

    # load in a mao
    self.iso.loadMap("maps/default")

    # create the minimap
    self.miniMap = Minimap(self.iso, -8, -8)




    # start game loop
    self.currentlySelecting = 0
    self.gameLoop()


  # start main loop
  def gameLoop(self):

    # local variables
    running = 1
    clock = pygame.time.Clock()

    # the loop
    while running:

      # set variables
      doSelection = 1

      # events
      for event in pygame.event.get():

        # quit game
        if event.type == QUIT: running = 0

        # resize screen
        elif event.type == VIDEORESIZE:
          s = pygame.display.set_mode(event.size, RESIZABLE)

        # general mouse move while clicking (left button)
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2]:
          self.iso.offsetX += event.rel[0]
          self.iso.offsetY += event.rel[1]
          self.currentCursor = self.cursorGrabber

        # general mouse move while clicking (left button)
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
          if self.miniMap.dragOnMap( event ): doSelection = 0
        else:
          self.currentCursor = self.cursorHand


        # test for selection
        if doSelection: self.selectionHandler(event)



      # bg and flush
      self.s.fill((120,120,120))

      # set the correct cursor
      pygame.mouse.set_cursor((16, 16), (0, 0), *self.currentCursor)

      # draw map
      self.iso.drawAll()

      # draw minimap
      self.miniMap.draw()

      # tick clock and flip buffers
      clock.tick()
      pygame.display.flip()


  # perform selection on the iso map
  def selectionHandler(self, event):
    # move mouse
    if event.type == pygame.MOUSEMOTION and not pygame.mouse.get_pressed()[2] and self.iso.selection and self.currentlySelecting and pygame.mouse.get_pressed()[0]:

      # mouse position
      mx, my = event.pos

      # get clicked tile
      tx, ty = self.iso.screenToIso(mx-self.iso.offsetX, my-self.iso.offsetY)

      # set selection area
      self.iso.selection[2] = int( tx - self.iso.selection[0] )
      self.iso.selection[3] = int( ty - self.iso.selection[1] )

      # see if any entities inside TODO LATER

    # selection code
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:#not pygame.mouse.get_pressed()[2]:

      # get clicked tile
      mx, my = event.pos
      tx, ty = self.iso.screenToIso(mx-self.iso.offsetX, my-self.iso.offsetY)
      fx, fy = self.iso.screenToIso(mx-self.iso.offsetX, my-self.iso.offsetY, asfloat=1)


      # first, see if the user clicked on an entity
      clickEntity = None
      for e in self.iso.entityList:
        if tx >= e.eX and ty >= e.eY and tx < e.eX + e.eWidth and ty < e.eY + e.eHeight:
          clickEntity = e

        # check for entitys inside
          if hasattr(clickEntity, "entityList"):

            for f in e.entityList:
              if tx >= e.eX + f.eX and ty >= e.eY + f.eY and fx < e.eX + f.eX + f.eWidth and fy < e.eY + f.eY + f.eHeight:
                clickEntity = f
                break


          break


      # user clicked on an entity
      if clickEntity:
        self.iso.selection = [int(clickEntity.eX), int(clickEntity.eY), int(clickEntity.eWidth), int(clickEntity.eHeight)]
        self.iso.selectedItems = [ clickEntity ]

      # start a normal selection
      elif not self.iso.selection and self.currentlySelecting == 0:
        self.iso.selection = [tx, ty, 0, 0]
        self.currentlySelecting = 1

      else:
        # clear selection
        self.iso.selection = None
        self.iso.selectedItems = None



    elif event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[2]:
      if self.iso.selection and self.currentlySelecting:
        # end selection
        self.currentlySelecting = 0




if __name__ == '__main__':
  Game()
