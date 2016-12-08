# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 00:24:43 2016

@author: abdelmajid
"""
import time



def get_timestap_utc():
    """
    Routourne le temps UTC. en entier (timestap).
    """
    return int(time.time()+time.altzone)
