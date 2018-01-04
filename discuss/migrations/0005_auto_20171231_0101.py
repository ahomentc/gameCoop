# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 01:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_categories_gatekeeper'),
        ('discuss', '0004_auto_20171230_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Categories'),
        ),
        migrations.AlterField(
            model_name='post',
            name='discussionType',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='DiscussionType',
        ),
    ]
