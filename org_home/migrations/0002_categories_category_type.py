# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org_home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='category_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
