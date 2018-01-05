# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from org_home.models import Categories
from .models import Post,Reply
from .forms import newPost,newMainReply

# org_home page of discussion. Show the "general" discussion.
def Index(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    no_posts_message = ''
    generalPostsList = Post.objects.filter(
            category=category,
            discussionType='General'
        ).order_by('-pub_date')[:10]
    if len(generalPostsList) == 0:
        no_posts_message = "No posts here yet"
    return render(request,'discuss/index.html',{'category': category,'postsList':generalPostsList,'no_posts_message':no_posts_message})

# the "idea" discussions
def IdeaDiscussion(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    no_posts_message = ''
    ideaPostsList = Post.objects.filter(
            category=category,
            discussionType='Idea'
        ).order_by('-pub_date')[:10]
    if len(ideaPostsList) == 0:
        no_posts_message = "No posts here yet"
    return render(request,'discuss/ideaDiscussion.html',{'category': category,'postsList':ideaPostsList,'no_posts_message':no_posts_message})

# the "voting" discussion
def VotingDiscussion(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    no_posts_message = ''
    votingPostsList = Post.objects.filter(
            category=category,
            discussionType='Voting'
        ).order_by('-pub_date')[:10]
    if len(votingPostsList) == 0:
        no_posts_message = "No posts here yet"
    return render(request,'discuss/ideaDiscussion.html',{'category': category,'postsList':votingPostsList,'no_posts_message':no_posts_message})

# page to create a new Post
def newPostView(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    form = newPost()
    return render(request,'discuss/newPost.html',{'category':category,'form':form})

# submit that post
def submitNewPost(request,category_id):
    category = get_object_or_404(Categories,pk=category_id)
    if request.method == "POST":
        form = newPost(request.POST)
        if form.is_valid():
            discussionType = request.POST['discussionType']
            Post.objects.create(
                discussionType=discussionType,
                category=category,
                title=request.POST['title'],
                content=request.POST['content'],
                pub_date=timezone.now(),
                original_poster=request.user
            )
            # go to the page that the post was created for
            if discussionType == 'Idea':
                return HttpResponseRedirect(reverse('discuss:IdeaDiscussion', args=(category.id,)))
            elif discussionType == 'Voting':
                return HttpResponseRedirect(reverse('discuss:VotingDiscussion', args=(category.id,)))
            else:
                return HttpResponseRedirect(reverse('discuss:Index', args=(category.id,)))
    else:
        form = newPost()
    return render(request,'discuss/newPost.html',{'category':category,'form':form})

# recursively get an infinitely nested dictionary of all the replies
def getRepliesNestedDict(highestList,post):
    tempDict = {}
    for element in highestList:
        subReplies = Reply.objects.filter(post=post,parent=element)
        if len(subReplies) == 0:
            tempDict[element] = None
        else:
            tempDict[element] = getRepliesNestedDict(subReplies,post)
    return tempDict

# returns a dictionary where the subdictionaries have been flattened to a list
def correctlyFormatDict(dict):
    print(dict)
    newDict = {}
    for key,value in dict.items():
        if value is None:
            newDict[key] = None
        else:
            newDict[key] = sorted(flattenDict(value),key=lambda x:x.pub_date,reverse=True)
    return newDict

# recursively flattens a dictionary that looks like this: {a:{b:None,c:{d:None}},e:None} to a list [a,b,c,d,e]
def flattenDict(dict):
    tempList = []
    for key,value in dict.items():
        tempList = tempList + [key]
        if value != None:
            tempList = tempList + flattenDict(value)
    return tempList

# shows an individual post and all the replies to it
def IndividualPost(request,category_id,post_id):
    category = get_object_or_404(Categories,pk=category_id)
    post = get_object_or_404(Post,pk=post_id)

    # list of replies that are not replies to a reply to the post
    noParentsList = Reply.objects.filter(post=post,parent__isnull=True).order_by('-pub_date')
    # dictionary with    keys: noParentsList items   values: list of all the replies to each key
    sortedDict = {}
    repliesDict = correctlyFormatDict(getRepliesNestedDict(noParentsList,post))
    for key in sorted(repliesDict.keys(),key=lambda x: x.pub_date):
        sortedDict[key] = repliesDict[key]


    form = newMainReply()
    return render(request,'discuss/individualPost.html',{'category':category,'post':post,'form':form,'repliesDict':sortedDict})

# submit a reply
def submitReply(request,category_id,post_id,parent_id=None):
    category = get_object_or_404(Categories,pk=category_id)
    post = get_object_or_404(Post,pk=post_id)

    # parent id is optional
    if parent_id is not None:
        parent = get_object_or_404(Reply,pk=parent_id)
    else:
        parent=None
    if request.method == "POST":
        form = newMainReply(request.POST)
        if form.is_valid():
            r = Reply.objects.create(
                post=post,
                parent=parent,
                content=request.POST['content'],
                user=request.user,
                pub_date=timezone.now()
            )
            return HttpResponseRedirect(reverse('discuss:IndividualPost', args=(category.id,post.id)))
    else:
        form = newMainReply()
    return render(request,'discuss/individualPost.html',{'category':category,'post':post,'form':form})
