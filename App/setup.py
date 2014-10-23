import sys
from cx_Freeze import setup,Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = 'KR Searcher',
version = '0.1',
description = 'aaaa',
executables = [Executable('main.py',base=base)])
