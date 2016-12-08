# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:11:43 2016

@author: abdelmajid
"""
from __future__ import unicode_literals

from django.db import models

# Create your models here.

 #================Model Client================  

class Client(models.Model):
    """Un modele pour les clients (victimes)"""
    id_client=models.AutoField(primary_key=True)
    ipadresse=models.CharField(verbose_name="Adresse IP du victime",max_length=100)
    hostname=models.CharField(verbose_name="Host du victime, ordinator name",max_length=100)
    connecte=models.BooleanField(default=True)
    
    #+++++++++++++++++++++++++++++++++
    class Meta:
        verbose_name = 'Client Victim'
        verbose_name_plural = 'Clients vectimes'
    
    #+++++++++++++++++++++++++++++++++
    def __unicode__(self):
        """représentation sous forme d'une chaine de caractere"""
        return u"Vectim: "+unicode(self.hostname)+", IP: "+unicode(self.ipadresse)+(unicode(", En ligne") if self.connecte else unicode(", Hors ligne"))
    
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        return u"Vectim: "+str(self.hostname)+", IP: "+str(self.ipadresse)+(", En ligne" if self.connecte else ", Hors ligne")
    
 #===============Model Message=================   
    
class Message(models.Model):
    """Les messages pour les victimes"""
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
        """représentation sous forme d'une chaine de caractere"""
        tx="********\nVectim: "+unicode(self.client)+"\n text: "+unicode(self.text)+", date: "+unicode(self.datem)+", Message "
        tx+=unicode("Vue") if self.vue else unicode("Non vue")
        return tx+"\n"
    #+++++++++++++++++++++++++++++++++
    def __str__(self):
        """représentation sous forme d'une chaine de caractere"""
        tx="********\nVectim: "+str(self.client)+"\n text: "+str(self.text)+", date: "+str(self.datem)+", Message "
        tx+="Vue" if self.vue else "Non vue"
        return u""+tx+"\n"
 
