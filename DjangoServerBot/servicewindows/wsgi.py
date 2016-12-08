# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:11:43 2016

@author: abdelmajid
"""
#----------------
"""
WSGI config for servicewindows project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicewindows.settings")

application = get_wsgi_application()
