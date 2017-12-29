# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    pending_members = models.ManyToManyField(User,related_name='pending_member')
    members = models.ManyToManyField(User,related_name='member')
    moderators = models.ManyToManyField(User,related_name='super_member')
    closed_category = models.BooleanField()
    gateKeeper = models.CharField(max_length=30) # either all_members or moderators

    def __str__(self):
        return self.category_name
