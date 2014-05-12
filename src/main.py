import pygame
from pygame.locals import *


def main():

  # init pygame
  pygame.init()

  # create surface
  s = pygame.display.set_mode((800, 400), RESIZABLE)

  # start main loop
  running = 1
  clock = pygame.time.Clock()
  t = None
  while running:

    # events
    for event in pygame.event.get():

      # quit game
      if event.type == QUIT: running = 0

      # resize screen
      elif event.type == VIDEORESIZE:
        s = pygame.display.set_mode(event.size, RESIZABLE)

      # move mouse
      elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[1]:
        wld.px += -event.rel[0]/64.0
        wld.py += -event.rel[1]/64.0




    # bg and flush
    s.fill((120,120,120))

    clock.tick()
    pygame.display.flip()
      

if __name__ == '__main__':
  main()
