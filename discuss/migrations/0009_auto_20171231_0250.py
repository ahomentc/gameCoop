# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 02:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discuss', '0008_auto_20171231_0247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='original_poster',
        ),
        migrations.AddField(
            model_name='post',
            name='original_poster',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]