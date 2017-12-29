# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from home.models import Categories
from django.contrib.auth.decorators import login_required

@login_required
def ProfileView(request):
    return render(request,'user_profiles/profile.html',{'member_categories_list': Categories.objects.filter(
        members__id=request.user.id)
    })
