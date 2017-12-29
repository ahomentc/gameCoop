# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

@login_required
def IndexView(request):
    return render(request, 'org_struct/index.html')

@login_required
def MoneyDistributionView(request):
    return render(request, 'org_struct/monetary_distribution.html')
