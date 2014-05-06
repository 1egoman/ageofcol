#!/usr/bin/python
# This is just the 'launcher', it just runs lib/main.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib') )
import main
m = main.main()
m.onexecute()