#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:11:43 2016

@author: abdelmajid
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicewindows.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
