## 0.1 Alpha
<TIMESTAMP>

#### Bugfixes
- Hovering over the minimap while selecting (with left-click) no longer causes the map to jerk

- Left-clicking on the minimap no longer selects tiles beneath it

#### New Features
- Implemented end-user/final-release-style debug output using easygui (see Miscellaneous below for link)

#### Optimization/Code-Cleanup
- Modularized GUI/Graphics handling
	- Entity drawing remains in their respective classes for efficiency reasons

- Other minor changes

#### Miscellaneous
- Added a folder for libraries in src

- Added the GUI library "Easygui" [easygui.sourceforge.net](easygui.sourceforge.net)

- Added preliminary FPS limit

- Updated README.md