from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'user_profiles'


urlpatterns = [
    url(r'^profile/$', views.ProfileView, name='ProfileView'),
]
