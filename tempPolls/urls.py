from django.conf.urls import url
from . import views

app_name = 'tempPolls'

urlpatterns = [
    url(r'^index$', views.index1, name='index'),
]
