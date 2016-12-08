# -*- coding:utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables_s = [
    Executable('winservice.py', base=base)
]

setup(name='Windows service ',
      version='0.1',
      description='Windows service',
      options={},
      executables=executables_s
      )
