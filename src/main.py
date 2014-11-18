from sys import exit
from traceback import print_exc

import pygame
from pygame.locals import *

from lib.easygui import exceptionbox
import isomap, entity, GUI
from minimap import Minimap


class Game(object):
  def __init__(self):
    # init pygame
    pygame.init()

    # create surface for screen
    self.s = pygame.display.set_mode((800, 600), RESIZABLE)

    # create the map
    self.iso = isomap.isoMap(8, 8)

    # load in a map
    self.iso.loadMap("maps/default")

    # create the minimap
    self.miniMap = Minimap(self.iso, -8, -8)

    # Create GUI manager
    self.GUI = GUI.GUI(self.s, self.iso, self.miniMap)

    # Create graphics handler
    self.graphics = GUI.Graphics(self.s, self.iso, self.miniMap)


    # start game loop
    self.gameLoop()



  # start main loop
  def gameLoop(self):

    # local variables
    running = True
    clock = pygame.time.Clock()

    # Debug control/output using traceback and lib.easygui
    try:
      # the loop
      while running:

        # set variables
        doSelection = True

        # events
        for event in pygame.event.get():

          # quit game
          if event.type == QUIT: running = False

          # resize screen
          elif event.type == VIDEORESIZE:
            self.s = pygame.display.set_mode(event.size, RESIZABLE)

          # Mouse movement
          elif event.type == pygame.MOUSEMOTION:
            self.GUI.handleMouseMtn(event, doSelection)

          # test for selection
          if doSelection: self.GUI.selectionHandler(event)



        # set the correct cursor
        pygame.mouse.set_cursor((16, 16), (0, 0), *self.GUI.currentCursor)

        # Renders graphics/GUI to screen
        self.graphics.render()

        # Ticks the game clock, keeps the FPS within the specified number
        clock.tick(100)

    except Exception:
      exceptionbox()
      print_exc()
      exit()


if __name__ == '__main__':
  Game()
