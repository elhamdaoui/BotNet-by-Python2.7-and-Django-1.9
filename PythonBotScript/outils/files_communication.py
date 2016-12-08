# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 00:07:43 2016

@author: abdelmajid
"""
import json

#==========
def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return None

#==========
def save_json(file_path, data, **kwargs):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, **kwargs)
            return True
    except:
        return False
