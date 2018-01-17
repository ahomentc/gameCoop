from django.conf.urls import url
from . import views

app_name = 'org_home'

urlpatterns = [
    url(r'^(?P<organization_id>\d+)/$', views.IndexView, name='index'),

    url(r'^(?P<organization_id>\d+)/categories$', views.CategoryView, name='categories'),
    url(r'^(?P<organization_id>\d+)/newCategory.html$',views.newCategoryView,name='newCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/newCategory.html$',views.newCategoryView,name='newSubCategory'),
    url(r'^(?P<organization_id>\d+)/submitNewCategory$',views.submitNewCategory,name='submitNewCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/submitNewCategory$',views.submitNewCategory,name='submitNewSubCategory'),

    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/$', views.IndividualCategoryView, name='individualCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/joinCategory$', views.JoinCategory, name='joinCategory'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/members$', views.membersView, name='membersView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/pendingMembers$', views.pendingMembersView, name='pendingMembersView'),
    url(r'^(?P<organization_id>\d+)/(?P<category_id>\d+)/(?P<pending_member_id>\d+)/grant_access$', views.GrantAccess, name='GrantAccess'),
]
