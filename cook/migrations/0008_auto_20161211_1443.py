# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 19:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0007_auto_20161211_1416'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Groups',
            new_name='Group',
        ),
    ]
