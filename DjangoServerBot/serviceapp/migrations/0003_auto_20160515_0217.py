# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 02:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0002_auto_20160514_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadExecution',
            fields=[
                ('id_ae', models.AutoField(primary_key=True, serialize=False)),
                ('date_insertion_ae', models.DateTimeField(auto_now_add=True, verbose_name='Date insertion')),
                ('vue', models.BooleanField(default=False)),
                ('emplacement', models.CharField(blank=True, max_length=256, null=True, verbose_name='emplacement')),
                ('results', models.TextField(blank=True, null=True, verbose_name='R\xe9sultats')),
                ('client_commande_ae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.ClientCommande')),
            ],
            options={
                'verbose_name': 'Download execution',
                'verbose_name_plural': 'Download executions',
            },
        ),
        migrations.AlterModelOptions(
            name='screenshotexecution',
            options={'verbose_name': 'Screenshot execution', 'verbose_name_plural': 'Screenshot executions'},
        ),
        migrations.AlterField(
            model_name='uploadexecution',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
