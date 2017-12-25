# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render

def ProfileView(request):
    return render(request,'user_profiles/profile.html')
