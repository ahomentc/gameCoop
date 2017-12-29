# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic,View
from django.db.models import F
from django.utils import timezone
from django.forms.formsets import formset_factory
from home import models as home_models
from django.contrib.auth.decorators import login_required

from .models import Choice, Question
from home.models import Categories

def is_member(func):
    def check(request,*args, **kwargs):
        if 'category_id' in kwargs:
            category = get_object_or_404(home_models.Categories,pk=kwargs['category_id'])
        try:
            if request.user in category.members.all():
                return func(request,*args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('home:individualCategory', args=(category.id,)))
        except:
            return HttpResponseRedirect(reverse('home:individualCategory', args=(category.id,)))
    check.__doc__=func.__doc__
    check.__name__=func.__name__
    return check


@is_member
@login_required
def IndexView(request,category_id):
    category = get_object_or_404(home_models.Categories,pk=category_id)
    return render(request,'vote/index.html',{
        'category': category, 'latest_question_list': Question.objects.filter(
            pub_date__lte=timezone.now(),category = category
        ).order_by('-pub_date')[:5]
    })

@is_member
@login_required
def DetailView(request,category_id,question_id):
    category = get_object_or_404(home_models.Categories,pk=category_id)
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'vote/detail.html',{
        'category': category,'question':question,'choice_set':Question.objects.filter(pub_date__lte=timezone.now())
    })

@is_member
@login_required
def ResultsView(request,category_id,question_id):
    category = get_object_or_404(home_models.Categories,pk=category_id)
    question = get_object_or_404(Question,pk=question_id)
    percentVoted = str((len(question.voters.all())/len(category.members.all()))*100)
    return render(request,'vote/results.html',{
        'category': category,'question':question,'choice_set':Question.objects.filter(pub_date__lte=timezone.now()),'percent_voted':percentVoted,
    })

@is_member
@login_required
def vote(request, category_id,question_id):
    question = get_object_or_404(Question, pk=question_id)
    category = get_object_or_404(Categories, pk=category_id)
    percentVoted = str(round(float(len(question.voters.all()))/float(len(category.members.all())) * 100,1))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'vote/detail.html', {
            'category': category,
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if request.user in question.voters.all():
            return render(request, 'vote/results.html', {
            'category': category,
            'question': question,
            'choice_set':Question.objects.filter(pub_date__lte=timezone.now()),
            'percent_voted':percentVoted,
            'error_message': "You have already voted",
        })
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        question.voters.add(request.user)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('vote:results', args=(category_id,question.id)))

@is_member
@login_required
def newPollView(request,category_id):
    category = get_object_or_404(home_models.Categories,pk=category_id)
    return render(request, 'vote/newPoll.html',{'category':category})

@is_member
@login_required
def submitNewPoll(request,category_id):
    category = get_object_or_404(home_models.Categories,pk=category_id)
    # make sure there is one question and at least two choices and that they aren't empty
    if 'question' in request.POST and 'choice_1' in request.POST and 'choice_2' in request.POST and request.POST['question'] != "" and request.POST['choice_1'] != "" and request.POST['choice_2'] != "":
        q = Question.objects.create(category = category, question_text=request.POST['question'], pub_date=timezone.now())
        # for every choice_ in POST, check to see if it isn't empty add this choice to the question created above
        for c in request.POST:
            if 'choice' in c and request.POST[c] != "":
                q.choice_set.create(choice_text = request.POST[c])
        # if everything works send to the index page
        return HttpResponseRedirect(reverse('vote:index', args=(category.id,)))
    else:
        # if error take back to newPoll page with error message
        return render(request, 'vote/newPoll.html', {
            'error_message': "Please enter a question and a two choices",
            'category': category
        })
