# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='closed_category',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]