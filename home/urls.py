from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),

    url(r'^categories$', views.CategoryView.as_view(), name='categories'),  #http://127.0.0.1.8000/vote/category
    url(r'^newCategory.html$',views.newCategoryView,name='newCategory'),
    url(r'^submitNewCategory$',views.submitNewCategory.as_view(),name='submitNewCategory'),

    url(r'^(?P<pk>\d+)/$', views.IndividualCategoryView, name='individualCategory'),
]
