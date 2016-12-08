# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 23:07:43 2016

@author: abdelmajid
"""

import requests

#url_loc="http://www.mon-ip.com/info-adresse-ip.php"
url_loc="http://www.hostip.fr/"

#=============
def getLocalisation():
    """localiser cet machine, retourne L'adresse ip ,le pays et la contenent"""
    r=None
    try:
        r=requests.get(url_loc)
        r.encoding="utf-8"
    except:
        r=None
    
    if r is not None and r.ok:
        ip,pays,continent="None","Inconnue","Inconnue"
        #part1=r.content.partition('<span id="ip">')
        #part1=part1[2][:100]
        #ip=part1.split("</span>")[0].strip()#
        #part1=r.content.partition('</strong></li>\r\n          <li>Zone G\xc3\xa9ographique :')
        #contenent=part1[2][:100].split('</li>\r\n')[0].strip()#
        #part1=r.content.partition('<li>Pays de Connexion :\r\n')
        #pays=part1[2][:100].split("<img")[0].strip()#
        part=r.content.split('<p>Adresse Ip<br><b>')[1]
        part=part.split("</p><p>Region<br><b>")[0]
        ip=part.split("</b></p><p>")[0]
        pays=part.split("</b></p><p>")[1].split("<br><b>")[1][:-4]
        return {"ip":ip,"pays":pays,"contenent":continent}
        #print "Salam: ip= %s , pays= %s, Zone= %s \n"%(ip,pays,contenent)
    return {"ip":"None","pays":"Inconnue","contenent":"Inconnue"}
