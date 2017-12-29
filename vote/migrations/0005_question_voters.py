# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 06:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0004_auto_20171223_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='voters',
            field=models.ManyToManyField(related_name='voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
