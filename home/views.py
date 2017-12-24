# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render

from .models import Categories

def IndexView(request):
    return render(request, 'home/index.html')

def IndividualCategoryView(request,pk):
    category = get_object_or_404(Categories,pk=pk)
    return render(request,'home/individualCategory.html',{'category': category})

class CategoryView(generic.ListView):
    template_name = 'home/categories.html'
    context_object_name = 'categories_list'

    def get_queryset(self):
        return Categories.objects.all()

def newCategoryView(request):
    return render(request, 'home/newCategory.html')

class submitNewCategory(View):
    def post(self, request, *args, **kwargs):
        if 'new_category_1' in request.POST and request.POST['new_category_1'] != '':
            Categories.objects.create(category_name=request.POST['new_category_1'])
            for c in request.POST:
                if 'new_category_' in c and request.POST[c] != "" and c != "new_category_1":
                    Categories.objects.create(category_name=request.POST[c])
            return HttpResponseRedirect(reverse('home:categories'))
        else:
            return render(request, 'home/newCategory.html', {
                'error_message': "Please enter at least one category.",
            })
