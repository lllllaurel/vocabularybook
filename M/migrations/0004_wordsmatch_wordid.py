# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-21 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('M', '0003_auto_20180521_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordsmatch',
            name='wordid',
            field=models.TextField(default=0),
        ),
    ]
