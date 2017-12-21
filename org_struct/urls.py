from django.conf.urls import url
from . import views

app_name = 'org_struct'

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),
]
