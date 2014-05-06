import pygame

class listdisplay(object):

  def __init__(self, screen, x, y, w, h, dlist):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.list = dlist
    self.screen = screen

    self.selecteditem = 0

  def render(self):

    pygame.draw.rect(self.screen, (180,180,180), (self.x, self.y-2, self.w, self.h))
    self.font = pygame.font.SysFont('monospace', 15)

    pygame.draw.rect(self.screen, (0, 180, 180), (self.x+5, self.y+(self.selecteditem*self.font.size("a")[1])-1, self.w-10, self.font.size("a")[1]+1))

    for ct,i in enumerate(self.list):
      rndr = self.font.render(i, True, (255,255,255))

      self.screen.blit(rndr, (self.x+10, self.y+(ct*rndr.get_height())))

  def event(self, event):

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mx, my = event.pos

      if mx <= self.w-20:
        self.selecteditem = (my-self.y)/(self.font.size("a")[1])
        if self.selecteditem < 0: self.selecteditem = 0
        # if selecteditem > 
