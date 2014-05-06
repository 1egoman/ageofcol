from entity import entityinstance, entity
import common
import pygame
import math

class guipipe(entityinstance):
  activecolor = (120,120,0)
  inactivecolor = (255,0,0)
  speed = 1

  def __init__(self, start, end):
    super(entityinstance, self).__init__()
    self.start = start
    self.end = end
    self.level = False
    self.angle = 0
    self.length = 0
    self.contents = []

    common.en.entitys.append(self)

  def switchends(self):
    s = self.start
    self.start = self.end
    self.end = s

  def render(self):
    # If a building is deleted than get rid of the pipe
    if self.start != None and self.start.deleting: self.start = None
    if self.end != None and self.end.deleting: self.end = None


    if self.start and self.end:

      # Calculate vector angle and length
      cx = (self.start.x+(self.start.w/2)) - (self.end.x+(self.end.w/2))-2
      cy = (self.start.y+(self.start.h/2)) - (self.end.y+(self.end.h/2))-2
      self.angle = -(math.degrees(math.atan2(cx, cy))+90)
      self.length = math.hypot(cx, cy)

      # self.x = self.start.x
      # self.y = self.start.y
      # self.w = cx
      # self.h = cy


      # Draw the pipe
      if self.contents:
        color = self.activecolor
      else:
        color = self.inactivecolor

      # Draw the pipe
      pygame.draw.aaline(common.screen, color, 
        (common.mapx+self.start.x+(self.start.w/2), common.mapy+self.start.y+(self.start.h/2)), 
        (common.mapx+self.end.x+(self.end.w/2), common.mapy+self.end.y+(self.end.h/2)), len(self.contents)+1)



      # if there is anything going 'through' the pipe, push it foreward
      if self.contents:
        for c,i in enumerate(self.contents):

          # get information about the item
          self.contents[c] = (i[0], i[1] + self.speed)
          Iid, length = self.contents[c]

          # Got to the end of the pipe
          if length >= self.length:
            self.contents.remove( self.contents[c] )
            self.end.inventory.additem(Iid, 1)

          # calculate position in the pipe
          ix = int(length * math.cos( math.radians(self.angle) ))
          iy = int(length * math.sin( math.radians(self.angle) ))

          itemloc = entity.itemslocation[ entity.itemsbyid[Iid] ]
          common.screen.blit(common.g.itemtiles, (common.mapx+self.start.x+(self.start.w/2)+ix, common.mapy+self.start.y+(self.start.h/2)+iy), (itemloc[0], itemloc[1], common.entitywidth, common.entitywidth) )


def getPipeAt(start, end=None, **kwargs):
  if kwargs.has_key('order'): order = True

  for p in [e for e in common.en.entitys if isinstance(e, guipipe)]:
    if p.start == start and p.end == end or p.start == start and end == None:
      return p