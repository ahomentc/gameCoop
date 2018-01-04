# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from home import models as home_models
from django.contrib.auth.models import User

class Post(models.Model):
    discussionType = models.CharField(max_length=100)
    category = models.ForeignKey(home_models.Categories,on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    original_poster = models.ForeignKey(User,blank=True,null=True)
    pub_date = models.DateTimeField('date published', blank=True, null=True)

class Reply(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True)
    content = models.TextField()
    user = models.ForeignKey(User,blank=True,null=True)
    pub_date = models.DateTimeField('data published',blank=True,null=True)
