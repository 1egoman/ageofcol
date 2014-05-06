try:
  import random, os, common, easygui
except UserWarning:
  pass




class PerlinNoiseGenerator:

    def __init__(self):

        self.noise = []
        self.noise_width = 0
        self.noise_height = 0

    def generate_noise(self, width, height, frequency, octaves):

        """Generates a 2d array of random noise."""

        del self.noise[:]
        self.noise_width = width
        self.noise_height = height

        for y in range(0, self.noise_height):
            noise_row = []
            for x in range(0, self.noise_width):
                noise_row.append(random.randint(0, 1000)/1000.0)
            self.noise.append(noise_row)

        result = []

        for y in range(0, self.noise_height):
            row = []
            for x in range(0, self.noise_width):
                row.append(self.turbulence(x*frequency,
                                               y*frequency,
                                               octaves))
            result.append(row)

        return result


    def smooth_noise(self, x, y):

        """Returns the average value of the 4 neighbors of (x, y) from the
           noise array."""

        fractX = x - int(x)
        fractY = y - int(y)

        x1 = (int(x) + self.noise_width) % self.noise_width
        y1 = (int(y) + self.noise_height) % self.noise_height

        x2 = (x1 + self.noise_width - 1) % self.noise_width
        y2 = (y1 + self.noise_height - 1) % self.noise_height

        value = 0.0
        value += fractX       * fractY       * self.noise[y1][x1]
        value += fractX       * (1 - fractY) * self.noise[y2][x1]
        value += (1 - fractX) * fractY       * self.noise[y1][x2]
        value += (1 - fractX) * (1 - fractY) * self.noise[y2][x2]

        return value


    def turbulence(self, x, y, size):

        """This function controls how far we zoom in/out of the noise array.
           The further zoomed in gives less detail and is more blurry."""

        value = 0.0
        size *= 1.0
        initial_size = size

        while size >= 1:
            value += self.smooth_noise(x / size, y / size) * size
            size /= 2.0

        return 128.0 * value / initial_size






def makeMap():
  args = ["World Name (Required)", "Width", "Height", "Seed", "World Generator String"]
  w,h=100,100

  watertable = 110
  biome_desert_level = 85
  biome_swamp_level = 100
  biome_forest_level = 125
  biome_flatland_level = 150
  biome_tiaga_level = 175
  biome_mountain_level = 255


  box = easygui.multenterbox("Leave Seed Blank for a Random Seed", "World Generator Settings", args)
  if not box: return
  print len(box)

  levelname = box[0]
  if len(box) >= 4 and box[3]: random.seed(box[3])
  if len(box) >= 2 and box[1]: 
    try:
      w = int(box[1])
    except ValueError:
      pass

  if len(box) >= 3 and box[2]: 
    try:
      h = int(box[2])
    except ValueError:
      pass

  if len(box) >= 5 and box[4]:
    try:
      watertable, biome_desert_level, biome_swamp_level, biome_forest_level, biome_flatland_level, biome_tiaga_level, biome_mountain_level = tuple([int(g) for g in box[4].split(";")])
    except ValueError: return

  try:
    os.mkdir(os.path.join(common.rootdir, "saves", levelname))
  except OSError:
    if easygui.ynbox("A World with the same name has already been created. Overwrite?", 'World Already Exists', ("Yes", "No")):
      pass
    else:
      return

  cxt = file(os.path.join(common.rootdir, "saves", levelname, "level.json"), "w+")


  sandlevel = watertable+10
  forestlevel = 150
  mtnlevel = 180
  octaves = 200
  tilewidth = 64
  nameone = ["Lema", "Mist", "North", "East", "South", "West", "Mil", "Barrow", "Iron", "Rock", "Harmon", "Center", "Cata", "Wilde", "Fox", "Way", "Dell", "Green", "Blue", "Land", "Merr", "Medow", "Gold", "By", "Winter", "Summer", "Spring", "Fall", "Mage", "Fun", "Lock", "Eri", "Clear", "Old", "Frey", "Sea", "Shell", "Haven", "Red", "Spen", "Syra", "Ron", "Stum", "Qwe", "Flat", "Tild"]
  nametwo = ["ville", "opilis", "town", "sis", "castle", "ilita", "ton", "port", "o", "uk", "burg", "borough"]


  mobchance = 50
  mob_biomes = ["flatland", "forest"]

  noise = PerlinNoiseGenerator().generate_noise(w,h,10,octaves)
  biomenoise = PerlinNoiseGenerator().generate_noise(w,h,5,octaves/3)
  mobs = [ [5,5,2] ]
  allowaquatic = True
  nbiome = None



  cxt.write('[{"map": [-270, -140]}, {"tiles": [')
  for x,c in enumerate(noise):
    for y,d in enumerate(c):

      # generate biomes
      if d <= watertable:
        if allowaquatic:
          biome = "aquatic"
        else:
          biome = nbiome
          allowaquatic = True

      elif biomenoise[x][y] <= biome_desert_level:
        biome = "desert"
        allowaquatic = True

      elif biomenoise[x][y] <= biome_swamp_level:
        biome = "swamp"
        allowaquatic = False
        nbiome = "swamp"

      elif biomenoise[x][y] <= biome_forest_level:
        biome = "forest"
        allowaquatic = True

      elif biomenoise[x][y] <= biome_flatland_level:
        biome = "grassland"
        allowaquatic = True
        
      elif biomenoise[x][y] <= biome_tiaga_level:
        biome = "tiaga"
        allowaquatic = True

      elif biomenoise[x][y] <= biome_mountain_level:
        biome = "mountain"
        allowaquatic = True

      else:
        biome = "unknown"
        allowaquatic = True


      # generate mobs
      if biome in mob_biomes and random.randrange(0, mobchance) == 0:
        mx = random.randrange(0, w*tilewidth)
        my = random.randrange(0, h*tilewidth)
        t = random.randrange(0, 3)

        try:
          if noise[mx/tilewidth][my/tilewidth] > watertable:
            mobs.append([mx,my,t])
        except IndexError:
          pass



      # generate tiles
      if d <= watertable:
        tile = "water"
        # water

      elif (d > watertable and d <= sandlevel) or (biome == "desert" and d > sandlevel):
        tile = "sand"
        # sand

      elif d > sandlevel and biome == "mountain": # biomenoise[x][y] > mtnlevel
          tile = "mountainhigh"
          # mountains

      elif d > sandlevel and (biome == "forest" or biome == "tiaga"): # biomenoise[x][y] > forestlevel 
          tile = "forest"
          if biome == "tiaga" and random.randrange(0, 3) == 0: tile = "grass"
          # forest

      elif d > sandlevel:
          tile = "grass"
          # grass

      else:
        tile = "none"
        # no tile?

      cxt.write('  {"x": '+str(x)+', "y": '+str(y)+', "tile": "'+tile+'", "biome": "'+str(biome)+'"}')
      if not ((not y != len(c)-1) and (not x != len(noise)-1)): 
        cxt.write(",")


  cxt.write(']}, {"structures": []},{"mobs": [')

  for c,m in enumerate(mobs):
    if m[2] == 0:
      ty = "pig"
    elif m[2] == 1:
      ty = "cow"
    elif m[2] == 2:
      ty = "unit"
    else:
      ty = "NoneType"

    if ty != "unit": 
      cxt.write('{"'+ty+'": [{"x": '+str(m[0])+'},{"y": '+str(m[1])+'},{"maxhealth": 100},{"health": 100},{"owner": "everyone"}]}')
    else:
      name = nameone[random.randrange(0, len(nameone))]+nametwo[random.randrange(0, len(nametwo))]
      cxt.write('{"'+ty+'": [{"x": '+str(m[0])+'},{"y": '+str(m[1])+'},{"maxhealth": 100},{"health": 100},{"owner": "'+name+'"}]}')

    if c != len(mobs)-1: cxt.write(",")

  cxt.write(']}, {"entitys": []}]')

  cxt.close()
  return levelname