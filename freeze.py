import sys, os
from cx_Freeze import setup, Executable
#sys.argv[1] = "build"

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),'main.py')
os.chdir(os.path.dirname(filename))

base = None
if sys.platform == "win32":
  base = "Win32GUI"


buildOptions = {"packages": ["os", "pygame", "sys", "json", "yaml", "urllib2"], "include_files": ["saves", "texturepacks", "lib"], 'create_shared_zip': False}

setup(
        name = "Age Of Colonization",
        version = "0.1",
        description = "Age of Colonization",
        options = dict(build_exe = buildOptions),
        executables = [Executable(filename, compress=True, base=base)]
)
