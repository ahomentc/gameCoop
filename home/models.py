# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    # pending_members = models.CharField()
    # members = models.CharField()
    closed_category = models.BooleanField()

    def __str__(self):
        return self.category_name
