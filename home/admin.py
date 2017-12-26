# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Categories

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_name'],}),
        (None,               {'fields': ['closed_category'],}),
    ]


admin.site.register(Categories, CategoryAdmin)

