from django.conf.urls import url
from . import views

app_name = 'vote'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)\/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)\/results$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>\d+)\/vote$', views.vote, name='vote'),
    # url(r'^newPoll$', views.newPollView, name='newPoll'),
    # url(r'^(?P<question_text>)\/submitNewPoll$',views.submitNewPoll, name='submitNewPoll'),
    url(r'^newPoll.html$',views.newPollView, name='newPoll'),
]
