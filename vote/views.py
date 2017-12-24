# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic,View
from django.db.models import F
from django.utils import timezone
from django.forms.formsets import formset_factory
from home import models as home_models

from .models import Choice, Question

# class IndexView(generic.ListView):
#     model = Categories
#     template_name = 'vote/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         """
#         Question.objects.filter(pub_date__lte=timezone.now()) returns a
#         queryset containing Questions whose pub_date is less than or equal to -
#         that is, earlier than or equal to - timezone.now.
#         """
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]

def IndexView(request,pk):
    category = get_object_or_404(home_models.Categories,pk=pk)
    return render(request,'vote/index.html',{
        'category': category, 'latest_question_list': Question.objects.filter(
            pub_date__lte=timezone.now(),category = category
        ).order_by('-pub_date')[:5]
    })

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'vote/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())

def DetailView(request,id,pk):
    category = get_object_or_404(home_models.Categories,pk=id)
    question = get_object_or_404(Question,pk=pk)
    return render(request,'vote/detail.html',{
        'category': category,'question':question,'choice_set':Question.objects.filter(pub_date__lte=timezone.now())
    })

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'vote/results.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())

def ResultsView(request,id,pk):
    category = get_object_or_404(home_models.Categories,pk=id)
    question = get_object_or_404(Question,pk=pk)
    return render(request,'vote/results.html',{
        'category': category,'question':question,'choice_set':Question.objects.filter(pub_date__lte=timezone.now())
    })


def vote(request, category_id,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'vote/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('vote:results', args=(category_id,question.id)))

def newPollView(request,pk):
    category = get_object_or_404(home_models.Categories,pk=pk)
    return render(request, 'vote/newPoll.html',{'category':category})

# class submitNewPoll(View):
#     def post(self, request, category):
#         # make sure there is one question and at least two choices and that they aren't empty
#         if 'question' in request.POST and 'choice_1' in request.POST and 'choice_2' in request.POST and request.POST['question'] != "" and request.POST['choice_1'] != "" and request.POST['choice_2'] != "":
#             q = Question.objects.create(question_text=request.POST['question'], pub_date=timezone.now(), category = category)
#             # for every choice_ in POST, check to see if it isn't empty add this choice to the question created above
#             for c in request.POST:
#                 if 'choice' in c and request.POST[c] != "":
#                     q.choice_set.create(choice_text = request.POST[c])
#             # if everything works send to the index page
#             return HttpResponseRedirect(reverse('vote:index'))
#         else:
#             # if error take back to newPoll page with error message
#             return render(request, 'vote/newPoll.html', {
#                 'error_message': "Please enter a question and a two choices",
#                 'category': category
#             })

def submitNewPoll(request,pk):
    category = get_object_or_404(home_models.Categories,pk=pk)
    # make sure there is one question and at least two choices and that they aren't empty
    if 'question' in request.POST and 'choice_1' in request.POST and 'choice_2' in request.POST and request.POST['question'] != "" and request.POST['choice_1'] != "" and request.POST['choice_2'] != "":
        q = Question.objects.create(category = category, question_text=request.POST['question'], pub_date=timezone.now())
        # for every choice_ in POST, check to see if it isn't empty add this choice to the question created above
        for c in request.POST:
            if 'choice' in c and request.POST[c] != "":
                q.choice_set.create(choice_text = request.POST[c])
        # if everything works send to the index page
        return HttpResponseRedirect(reverse('vote:index', args=(pk)))
    else:
        # if error take back to newPoll page with error message
        return render(request, 'vote/newPoll.html', {
            'error_message': "Please enter a question and a two choices",
            'category': category
        })
