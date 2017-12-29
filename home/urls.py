from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),

    url(r'^categories$', views.CategoryView, name='categories'),
    url(r'^newCategory.html$',views.newCategoryView,name='newCategory'),
    url(r'^submitNewCategory$',views.submitNewCategory,name='submitNewCategory'),

    url(r'^(?P<category_id>\d+)/$', views.IndividualCategoryView, name='individualCategory'),
    url(r'^(?P<category_id>\d+)/joinCategory$', views.JoinCategory, name='joinCategory'),
    url(r'^(?P<category_id>\d+)/members$', views.membersView, name='membersView'),
    url(r'^(?P<category_id>\d+)/pendingMembers$', views.pendingMembersView, name='pendingMembersView'),
    url(r'^(?P<category_id>\d+)/(?P<pending_member_id>\d+)/grant_access$', views.GrantAccess, name='GrantAccess'),
]
