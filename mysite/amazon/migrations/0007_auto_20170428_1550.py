# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0006_auto_20170427_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whstock',
            name='whnum',
        ),
        migrations.AddField(
            model_name='whstock',
            name='ctlg',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='whstock',
            name='wid',
            field=models.BigIntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='whstock',
            name='dsc',
            field=models.CharField(default='', max_length=100),
        ),
    ]
