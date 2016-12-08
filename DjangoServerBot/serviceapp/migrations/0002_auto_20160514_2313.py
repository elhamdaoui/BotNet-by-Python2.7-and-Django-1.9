# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-14 23:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadExecution',
            fields=[
                ('id_ae', models.AutoField(primary_key=True, serialize=False)),
                ('date_insertion_ae', models.DateTimeField(auto_now_add=True, verbose_name='Date insertion')),
                ('vue', models.BooleanField(default=False)),
                ('fichier', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('results', models.TextField(verbose_name='R\xe9sultats')),
                ('client_commande_ae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.ClientCommande')),
            ],
            options={
                'verbose_name': 'Upload execution',
                'verbose_name_plural': 'Upload executions',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='src',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Chemin de bot'),
        ),
    ]
