# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 08:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_categories_super_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='super_members',
            new_name='moderators',
        ),
    ]
