# -*- coding: utf-8 -*-
"""
Created on Thur Apr 28 22:25:43 2016

@author: abdelmajid
"""
import time,datetime
from serviceapp.models import *

#=====================
def ajouter_client(donnees):
    """
    ajouter un client, depuis le dictionnaire donnees.
    """
    if donnees is not None:
        cli=Client()
        if "hostname" in donnees:
            cli.hostname=donnees['hostname'][0]
        if "ville" in donnees:
            cli.ville=donnees['ville'][0]
        if "USERDOMAIN" in donnees:
            cli.USERDOMAIN=donnees['USERDOMAIN'][0]
        if "USERNAME" in donnees:
            cli.USERNAME=donnees['USERNAME'][0]
        if "PROCESSOR_IDENTIFIER" in donnees:
            cli.PROCESSOR_IDENTIFIER=donnees['PROCESSOR_IDENTIFIER'][0]
        if "PROCESSOR_REVISION" in donnees:
            cli.PROCESSOR_REVISION=donnees['PROCESSOR_REVISION'][0]
        if "PROCESSOR_ARCHITECTURE" in donnees:
            cli.PROCESSOR_ARCHITECTURE=donnees['PROCESSOR_ARCHITECTURE'][0]
        if "NUMBER_OF_PROCESSORS" in donnees:
            cli.NUMBER_OF_PROCESSORS=donnees['NUMBER_OF_PROCESSORS'][0]
        if "processor_level" in donnees:
            cli.processor_level=donnees['processor_level'][0]
        if "system" in donnees:
            cli.syetem=donnees['system'][0]
        if "src" in donnees:
            cli.src=donnees['src'][0]
        try:
            cli.save()
            gerer_ip_pays_content_client(cli,donnees)
            return cli
        except:
            return None

    return None

#=====================
def gerer_ip_pays_content_client(cli,donnees):
    """
    Tester si l'ip est deja existe et le mm chose pour pays et contenent, et on modifier ...:.
    """
    #---gerer pays et contenent
    p,c=None,None
    if "pays" in donnees:
        pays=donnees['pays'][0]
        try:
            p=Pays.objects.get(nom=pays)
        except:
            if "continent" in donnees:
                cont=donnees['continent'][0]
                try:
                    c=Continent.objects.get(nom=cont)
                except:
                    c=Continent.objects.create(nom=cont)
            else:
                try:
                    c=Continent.objects.get(nom="Inconnue")
                except:
                    c=Continent.objects.create(nom="Inconnue")
            p=Pays.objects.create(nom=pays,continent=c)
        cli.pays=p
        cli.save()
    #----gerer l'adresse ip
    iploc,ipinter,iprecu="None","None","None"
    if "iploc" in donnees and "ipinter" in donnees:
        iploc,ipinter=donnees['iploc'][0],donnees['ipinter'][0]
        if "iprecu" in donnees:
            iprecu=donnees['iprecu'][0]
        ip=None
        try:
            ip=IpAdresse.objects.get(ip_locale=iploc,ip_recue=iprecu,ip_inter=ipinter)
        except:
            ip=IpAdresse.objects.create(ip_locale=iploc,ip_recue=iprecu,ip_inter=ipinter)
        cli.ipadresse=ip
    #--- enregistrer les modificatiosn
    cli.save()

#----------------------
def infos_to_text(cli):
    """
    Tranformer les infos que l'agent a besions en texte formaté.
    """
    infos=list()
    infos.append('id_client:'+unicode(cli.id_client))
    infos.append('actif:'+unicode(cli.actif))
    infos.append('connecte:'+unicode(cli.connecte))
    return "{/ATTRIBUT/}".join(infos)

#----------------------
def commande_to_text(cmd):
    """
    fonction pour transformer une commande en texte pour l'envoyer au agent.
    """
    liste=[]
    d_b=date_to_int(cmd.date_debut)
    d_f=date_to_int(cmd.date_fin)
    d_d=date_to_int(cmd.duree)
    if type(d_d) is int:
        d_f=d_b+d_d#si il y a une duree, donc la date fin sera la date debut + duree

    liste.append("id_cmd:"+unicode(cmd.id_cmd))
    liste.append("type_cmd:"+unicode(cmd.type_cmd.nom))
    liste.append("titre:"+unicode(cmd.titre))
    liste.append("active:"+unicode(cmd.active))
    #le champ texte, et pour resudre tous les prb de manque d'attributs.
    liste.append("texte:"+unicode(cmd.texte))
    liste.append("date_debut:"+unicode(d_b))
    liste.append("date_fin:"+unicode(d_f))
    liste.append("duree:"+unicode(d_d))
    liste.append("url:"+unicode(cmd.url))
    return "{/ATTRIBUT/}".join(liste)

#-----------------------
def commandes_a_executer_to_text(cli):
    """
    recuperer toutes les commandes non executer et actives d'un agnet;
    et les tranformer en textes pour les envoyer.
    """
    if not cli.actif:
        return ""
    commandes=list()
    cmds=cli.clientcommande_set.all()
    for clicmd in cmds:
        if clicmd.executee == False:
            cmd=clicmd.commande
            if cmd.active:
                commandes.append(commande_to_text(cmd))
    return "{/COMMANDE/}".join(commandes)

#---------------------
def text_envoyer_gerer_agent(cli):
    """
    C'est le text formaté à envoyer au agent.
    """
    text="{/INFOS/}"+infos_to_text(cli)+"{/INFOS/}"
    text+="{/COMMANDES/}{/COMMANDE/}"+commandes_a_executer_to_text(cli)+"{/COMMANDE/}{/COMMANDES/}"
    return text

#----------------------
def date_to_int(d):
    """
    Convertir une date en un entier (timestap).
    """
    if type(d)==datetime.datetime:
        return int(time.mktime(d.timetuple()))+int(time.altzone)
    return d
