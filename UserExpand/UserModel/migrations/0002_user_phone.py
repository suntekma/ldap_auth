# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-26 03:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=13, null=True),
        ),
    ]
