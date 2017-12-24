from django.conf.urls import url
from . import views

app_name = 'vote'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.IndexView, name='index'),   #http://127.0.0.1:8000/vote/categories/2
    url(r'^(?P<id>\d+)/(?P<pk>\d+)\/$', views.DetailView, name='detail'),
    url(r'^(?P<id>\d+)/(?P<pk>\d+)\/results$', views.ResultsView, name='results'),
    url(r'^(?P<category_id>\d+)/(?P<question_id>\d+)\/vote$', views.vote, name='vote'),

    url(r'^(?P<pk>\d+)/newPoll.html$',views.newPollView, name='newPoll'),
    url(r'^(?P<pk>\d+)/submitNewPoll$', views.submitNewPoll, name='submitNewPoll'),
]
