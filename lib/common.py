#!/usr/bin/python
import os


running = False
screen = None

bypasslauncher = True
inlauncher = False
name = "Age of Colonization"
version = "0.3A"
width = 1000
height = 800
username = "player"
cursor = "arrow"
levelname = "default"
hiddengui = False
srclocation = ""
pausemenu = None
quitToLauncher = False

debug = False
isdebugallowed = False
debugtext = "Debug Text"
fps = 0 # if 0 no fps limit
keyreadpersec = 30
movespeed = 10
maxmovespeed = 30
structures = []
entitys = []
time = 0.0

mapx = width/2
mapy = height/2
tilewidth = 64
entitywidth = 24
mapw, maph = 1, 1
showminimap = False

mmapscale = 10
# Increase minimap size below....
mmapw = 20
mmapoffset = 0
mmaph = mmapw
mmaptilewidth = mmapw/10
mmapx = 5
mmapy = (height-mmaph-5)
mmaptile = 0

paused = False

selectedtext = "Nothing Selected"
selected = None
selectedtwo = None

seltool = 0
activetool = None

morepanel=False
mptab=0
toolbarwidth=9

infobox = None
infoboxX = 0
infoboxY = 0

chatbar = None
maxposts = 5
reverseposts = False

rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

enablesky = True
