# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
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
        if 'new_category' in request.POST and request.POST['new_category'] != '':
            closedCategory = False
            if 'closed_category' in request.POST:
                closedCategory = True
            categoryName =  request.POST['new_category']
            formatedCategoryName = ' '.join(word[0].upper() + word[1:] for word in categoryName.split())
            if Categories.objects.filter(category_name=formatedCategoryName).exists():
                return render(request, 'home/newCategory.html', {'error_message': formatedCategoryName + " already exists.",})
            Categories.objects.create(category_name=formatedCategoryName,closed_category = closedCategory)
            return HttpResponseRedirect(reverse('home:categories'))
        else:
            return render(request, 'home/newCategory.html', {
                'error_message': "Please enter at least one category.",
            })


def JoinCategory(request,category_pk):
    '''
    if accept anyone add user to members list of category
    if don't accept anyone add user to pending_members list of category
    '''

    category = get_object_or_404(Categories,pk=id)

