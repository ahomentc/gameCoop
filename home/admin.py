# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Categories
from vote.models import Question

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3

class ModeratorsInline(admin.TabularInline):
    model = Categories.moderators.through

class MembersInline(admin.TabularInline):
    model = Categories.members.through

class PendingMembersInline(admin.TabularInline):
    model = Categories.pending_members.through


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_name'],}),
        (None,               {'fields': ['closed_category'],}),
        (None,               {'fields': ['gateKeeper'],}),
    ]
    inlines = [QuestionInline,ModeratorsInline,MembersInline,PendingMembersInline]

admin.site.register(Categories, CategoryAdmin)

