import pygame

from entity import Entity
from dialogSpawner import checkToSpawnDialog, drawDialog


class GUI(object):
  '''
  Handles most user interactions with the game.
  '''
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


  def __init__(self, screen, iso_inst, minimap_inst):
    # compile cursors
    self.cursorHand = pygame.cursors.compile(self.hand_str, 'x', '.', "o")
    self.cursorGrabber = pygame.cursors.compile(self.grabber_str, 'x', '.', "o")
    self.currentCursor = self.cursorHand

    # Local name for the screen surface
    self.s = screen

    # Local names for objects
    self.iso = iso_inst
    self.miniMap = minimap_inst

    # Boolean used for "selection-mode" of tiles and entities
    self.currentlySelecting = False


  # General mouse motion
  def handleMouseMtn(self, event, doSelection):
    # While clicking right button
    if pygame.mouse.get_pressed()[2]:
      self.iso.offsetX += event.rel[0]
      self.iso.offsetY += event.rel[1]
      self.currentCursor = self.cursorGrabber

    # While clicking left button
    elif pygame.mouse.get_pressed()[0]:
      if not self.currentlySelecting and self.miniMap.dragOnMap(event, self.s): doSelection = False

    else:
      self.currentCursor = self.cursorHand



  # perform selection on the iso map
  def selectionHandler(self, event):
    # move mouse
    if event.type == pygame.MOUSEMOTION:
      if not pygame.mouse.get_pressed()[2] and self.iso.selection and self.currentlySelecting and pygame.mouse.get_pressed()[0]:

        # mouse position
        mx, my = event.pos

        # get clicked tile
        tx, ty = self.iso.screenToIso(mx-self.iso.offsetX, my-self.iso.offsetY)

        # set selection area
        self.iso.selection[2] = int( tx - self.iso.selection[0] )
        self.iso.selection[3] = int( ty - self.iso.selection[1] )

        # TODO: see if any entities inside

    # selection code
    elif event.type == pygame.MOUSEBUTTONDOWN and not self.miniMap.isOver(event, self.s) and event.button == 1 and not pygame.mouse.get_pressed()[2]:
      # get clicked tile
      mx, my = event.pos
      tx, ty = self.iso.screenToIso(mx-self.iso.offsetX, my-self.iso.offsetY)
      fx, fy = self.iso.screenToIso(mx-self.iso.offsetX, my-self.iso.offsetY, asfloat=1)


      clickEntity = None
      # first, see if the user clicked on an entity
      for e in sorted(self.iso.entityList, key=lambda x: x.sortOrder, reverse=True):
        # check for parent
        if hasattr(e, "parentEntity") and e.parentEntity:
          entX = e.eX + e.parentEntity.eX
          entY = e.eY + e.parentEntity.eY
        else:
          entX = e.eX
          entY = e.eY

        if tx >= entX and ty >= entY and tx < entX + e.eWidth and ty < entY + e.eHeight:
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
      elif not self.iso.selection and self.currentlySelecting == False:
        self.iso.selection = [tx, ty, 0, 0]
        self.currentlySelecting = True

      else:
        # clear selection
        self.iso.selection = None
        self.iso.selectedItems = None


    elif event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[2]:
      if self.iso.selection and self.currentlySelecting:
        # end selection
        self.currentlySelecting = False






class Graphics(object):
  '''
  Controls most rendering to the pygame display.
  '''
  def __init__(self, screen, iso_inst, minimap_inst):
    # self.s = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    self.s = screen

    # Local names for objects
    self.iso = iso_inst
    self.miniMap = minimap_inst


  # Draw stuff to the screen surface
  def render(self):
    # bg and flush
    self.s.fill((120,120,120))

    # Draw Isomap & tiles
    self.drawIsoMap()

    # Draw entities
    # Iterate through list of entities
    for e in self.iso.entityList:
      # if e is of type Entity or is a sibling of Entity
      if e.__class__ == Entity or Entity in e.__class__.__bases__:
        e.draw(self.s)


    # Draw any dialogs
    checkToSpawnDialog(self.iso)
    drawDialog(self.s)

    # Draw minimap
    self.drawMinimap()


    # Flip buffers
    pygame.display.flip()




  # draws the map & tiles to the screen
  def drawIsoMap(self):
    # loop through each tile
    for i in xrange(self.iso.mapWidth-1, -1, -1):
      for j in xrange(0, self.iso.mapHeight):

        # get tile position
        Cx, Cy = self.iso.IsoToScreen(i, j)

        # get tile name, and respective surface
        tileName = self.iso._tiles[i][j]["name"]
        tileSurface = self.iso.mapResources["tiles"][tileName]

        # get surface's position
        Tx = Cx + self.iso.offsetX
        Ty = Cy + self.iso.offsetY - tileSurface.get_height() + self.iso.tileHeight + self.iso.tileHeight/4

        # draw the tile
        self.s.blit(tileSurface, (Tx, Ty))


        # render borders
        if self.iso.renderBorders:

          # create the iso tile shape
          tilePoints = self.iso.getIsometricShape(Cx, Cy)

          # draw the border
          pygame.draw.polygon(self.s, (0, 0, 0), tilePoints, 1)


    # draw selection area
    if self.iso.selection:

      # make sure that the selection can never reach zero in size
      if self.iso.selection[2] == 0: self.iso.selection[2] = 1
      if self.iso.selection[3] == 0: self.iso.selection[3] = 1

      # this calculates the correct iterator to use in the for loop
      # depending on if the size of the x selection is positive or negitive
      if self.iso.selection[2] > 0:
        iterX = xrange(self.iso.selection[2]-1, -1, -1)
      else:
        iterX = xrange(self.iso.selection[2]-1, 1, 1)


      # this calculates the correct iterator to use in the for loop
      # depending on if the size of the y selection is positive or negitive
      if self.iso.selection[3] > 0:
        iterY = xrange(0, self.iso.selection[3], 1)
      else:
        iterY = xrange(0, self.iso.selection[3], -1)


      # loop through tiles
      for i in iterX:
        for j in iterY:

          # get tile position
          Cx, Cy = self.iso.IsoToScreen( self.iso.selection[0] + i, self.iso.selection[1] + j )

          # create the iso tile shape
          tilePoints = self.iso.getIsometricShape(Cx, Cy)

          # draw the border
          pygame.draw.polygon(self.s, (10, 158, 191), tilePoints, 4)





  # Renders the minimap
  def drawMinimap(self):
    # y offset so that it will render in the right place
    Yoff = (self.iso.mapHeight * self.miniMap.tileHeight)/2

    # calculate our difference in offset, and size
    ratio = self.iso.tileWidth*1.0 / self.miniMap.tileWidth
    Rx = int(self.iso.offsetX / ratio)
    Ry = int(self.iso.offsetY / ratio) - (self.iso.mapHeight / 2) * self.miniMap.tileHeight
    Rw = int(self.s.get_width() / ratio)
    Rh = int(self.s.get_height() / ratio)


    # parse the screen coords
    Sx, Sy = self.miniMap.getScreenPos(self.s)


    # create surface to draw upon
    mapSurf = pygame.Surface((Rw, Rh), pygame.SRCALPHA)
    mapSurf.fill((96, 96, 96, 200))

    # loop through each tile
    for i in xrange(self.iso.mapWidth-1, -1, -1):
      for j in xrange(0, self.iso.mapHeight): 

        # convert iso coords to screen coords
        Cx = (j+i)*(self.miniMap.tileWidth/2)
        Cy = (j-i)*(self.miniMap.tileHeight/2)

        # get the isometric shape
        tilePoints = [
          (Rx + Cx+self.miniMap.tileWidth/2, Ry + Yoff + Cy),
          (Rx + Cx+self.miniMap.tileWidth,   Ry + Yoff + Cy+self.miniMap.tileHeight/2),
          (Rx + Cx+self.miniMap.tileWidth/2, Ry + Yoff + Cy+self.miniMap.tileHeight),
          (Rx + Cx,                  Ry + Yoff + Cy+self.miniMap.tileHeight/2)
        ]

        # get tile name
        tileName = self.iso._tiles[i][j]["name"]

        # find the tile's color
        color = list( self.miniMap.averageTile[tileName][:3] )
        color.append(200) # set alpha

        # render tile
        pygame.draw.polygon(mapSurf, color, tilePoints)


    # draw Map to the screen
    self.s.blit(mapSurf, (Sx-Rw, Sy-Rh))

    # draw border
    pygame.draw.rect(self.s, (64, 64, 64), (Sx-Rw, Sy-Rh, Rw, Rh), 4)