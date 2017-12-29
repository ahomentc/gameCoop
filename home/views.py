# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Categories

@login_required
def IndexView(request):
    return render(request, 'home/index.html',{'member_categories_list': Categories.objects.filter(
        members__id=request.user.id)
    })

@login_required
def IndividualCategoryView(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'home/individualCategory.html',{'category': category})

@login_required
def CategoryView(request):
    return render(request,'home/categories.html',{'categories_list':Categories.objects.all()})

@login_required
def newCategoryView(request):
    return render(request, 'home/newCategory.html')

@login_required
def submitNewCategory(request):
    if 'new_category' in request.POST and request.POST['new_category'] != '':
        closedCategory = False
        gate_keeper = ''
        if 'closed_category' in request.POST:
            closedCategory = True
            gate_keeper = request.POST['access']
        categoryName =  request.POST['new_category']
        formatedCategoryName = ' '.join(word[0].upper() + word[1:] for word in categoryName.split())
        if Categories.objects.filter(category_name=formatedCategoryName).exists():
            return render(request, 'home/newCategory.html', {'error_message': formatedCategoryName + " already exists.",})
        category = Categories.objects.create(category_name=formatedCategoryName,closed_category = closedCategory,gateKeeper=gate_keeper)
        category.members.add(request.user)
        category.moderators.add(request.user)
        return HttpResponseRedirect(reverse('home:categories'))
    else:
        return render(request, 'home/newCategory.html', {
            'error_message': "Please enter at least one category.",
        })

@login_required
def membersView(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'home/members.html',{'category': category})

@login_required
def pendingMembersView(request,category_id):
    # this html is also called in GrantAccess
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'home/pendingMembers.html',{'category': category})

@login_required
def JoinCategory(request,category_id):
    '''
    if accept anyone add user to members list of category
    if don't accept anyone add user to pending_members list of category
    '''
    category = get_object_or_404(Categories,pk=category_id)
    # if category is open
    if category.closed_category == False:
        category.members.add(request.user)
    else:
        category.pending_members.add(request.user)
    return HttpResponseRedirect(reverse('home:individualCategory', args=(category.id,)))

@login_required
def GrantAccess(request,category_id,pending_member_id):
    category = get_object_or_404(Categories,pk=category_id)
    pending_member = User.objects.get(pk=pending_member_id)
    if category.gateKeeper == 'all_members':
        if request.user in category.members.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
    elif category.gateKeeper == 'moderators':
        if request.user in category.moderators.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
        else:
            return render(request,'home/pendingMembers.html',{'category': category,'error_message':'Must be a moderator to add user to ' +  category.category_name })
    return HttpResponseRedirect(reverse('home:pendingMembersView', args=(category.id,)))
