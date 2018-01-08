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
from home.models import Organizations

# org_home page of a coop
@login_required
def IndexView(request,organization_id):
    organization = get_object_or_404(Organizations,pk=organization_id)
    return render(request, 'org_home/index.html',{'organization': organization,'member_categories_list': Categories.objects.filter(
        members__id=request.user.id,organization=organization)
    })

# list of all the categories/root/branch in a coop
@login_required
def CategoryView(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request,'org_home/categories.html',{'organization':organization,'categories_list':Categories.objects.filter(organization=organization)})

# org_home page of specific category/root/branch in a coop
@login_required
def IndividualCategoryView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_home/individualCategory.html',{'organization':organization,'category': category})

# page to create a new category/root/branch
@login_required
def newCategoryView(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    return render(request, 'org_home/newCategory.html',{'organization':organization})

# submit a new category
@login_required
def submitNewCategory(request,organization_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    if 'new_category' in request.POST and request.POST['new_category'] != '':
        closedCategory = False
        gate_keeper = ''
        # closed_category is a checkbox of if people need persmission to join the category
        if 'closed_category' in request.POST:
            closedCategory = True
            # gate_keeper is who can let people join the community. It can either be anyone in the community
            # or the moderator. access is the name of the radio field
            gate_keeper = request.POST['access']

        categoryName =  request.POST['new_category']
        # first word in category name uppercased
        formatedCategoryName = ' '.join(word[0].upper() + word[1:] for word in categoryName.split())

        # returns error if the category name already exists
        if Categories.objects.filter(category_name=formatedCategoryName).exists():
            return render(request, 'org_home/newCategory.html', {'organization':organization,'error_message': formatedCategoryName + " already exists.",})

        # create the category, add the creator to the members list, and make the creator a moderator
        category = Categories.objects.create(organization = organization, category_name=formatedCategoryName,closed_category = closedCategory,gateKeeper=gate_keeper)
        category.members.add(request.user)
        category.moderators.add(request.user)
        return HttpResponseRedirect(reverse('org_home:categories', args=(organization.id,)))
    else:
        return render(request, 'org_home/newCategory.html', {
            'organization':organization,
            'error_message': "Please enter at least one category.",
        })

# list of all members in a category
@login_required
def membersView(request,organization_id,category_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_home/members.html',{'organization':organization,'category': category})

# list of pending members in a category
@login_required
def pendingMembersView(request,organization_id,category_id):
    # this html is also called in GrantAccess
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    return render(request,'org_home/pendingMembers.html',{'organization':organization,'category': category})

# join a category
@login_required
def JoinCategory(request,organization_id,category_id):
    '''
    if open category, add user to members list of category
    if closed category, add user to pending_members list of category
    '''
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    # if category is open
    if category.closed_category == False:
        category.members.add(request.user)
    else:
        category.pending_members.add(request.user)
    return HttpResponseRedirect(reverse('org_home:individualCategory', args=(organization.id,category.id,)))

# grant access to someone to become a member
@login_required
def GrantAccess(request,organization_id,category_id,pending_member_id):
    organization = get_object_or_404(Organizations,id=organization_id)
    category = get_object_or_404(Categories,pk=category_id)
    pending_member = User.objects.get(pk=pending_member_id)

    # if any member can add pending members to category
    if category.gateKeeper == 'all_members':
        if request.user in category.members.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
    # if only moderator can add pending members to category
    elif category.gateKeeper == 'moderators':
        if request.user in category.moderators.all():
            category.members.add(pending_member)
            category.pending_members.remove(pending_member)
        else:
            return render(request,'org_home/pendingMembers.html',{'organization':organization,'category': category,'error_message':'Must be a moderator to add user to ' +  category.category_name })
    return HttpResponseRedirect(reverse('org_home:pendingMembersView', args=(organization.id,category.id,)))
