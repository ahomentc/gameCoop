# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
from django.forms.formsets import formset_factory

from .models import Choice, Question



class IndexView(generic.ListView):
    template_name = 'vote/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        """
        Question.objects.filter(pub_date__lte=timezone.now()) returns a 
        queryset containing Questions whose pub_date is less than or equal to - 
        that is, earlier than or equal to - timezone.now.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'vote/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'vote/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
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
        return HttpResponseRedirect(reverse('vote:results', args=(question.id,)))

def newPollView(request):
    return render(request, 'vote/newPoll.html')

def submitNewPoll(request):
    if 'question' in request.POST and 'choice_1' in request.POST and 'choice_2' in request.POST and request.POST['question'] != "" and request.POST['choice_1'] != "" and request.POST['choice_2'] != "":
        q = Question.objects.create(question_text=request.POST['question'], pub_date=timezone.now())
        for c in request.POST:
            if 'choice' in c:
                q.choice_set.create(choice_text = request.POST[c])
        return HttpResponseRedirect(reverse('vote:index'))
    else:
        return render(request, 'vote/newPoll.html', {
            'error_message': "Please enter a question and a choice",
        })
