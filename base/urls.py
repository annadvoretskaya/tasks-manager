from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from base import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='base:projects-list'), name='projects-redirect'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),

    url(r'^projects/$', views.ProjectsListView.as_view(), name='projects-list'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^projects/(?P<pk>\d+)/invite/$', views.CreateInviteView.as_view(), name='project-invite'),
    url(r'^projects/(?P<pk>\d+)/update/$', views.UpdateProjectView.as_view(), name='project-update'),
    url(r'^projects/(?P<pk>\d+)/delete/$', views.DeleteProjectView.as_view(), name='project-delete'),
    url(r'^projects/new/$', views.CreateProjectView.as_view(), name='project-create'),
    url(r'^join/(?P<pk>[\w-]+)/$', views.JoinProjectView.as_view(), name='project-join'),

    url(r'^projects/(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/$', views.DetailTaskView.as_view(), name='task-detail'),
    url(r'^projects/(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/update/$', views.UpdateTaskView.as_view(), name='task-update'),
    url(r'^projects/(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/delete/$', views.DeleteTaskView.as_view(), name='task-delete'),
    url(r'^projects/(?P<project_pk>\d+)/tasks/new/$', views.CreateTaskView.as_view(), name='task-create'),

    url(r'^projects/(?P<project_pk>\d+)/members/((?P<pk>\d+))/remove$', views.RemoveMemberFromProjectView.as_view(),
        name='member-remove'),
    url(r'^projects/(?P<project_pk>\d+)/members/((?P<pk>\d+))/change', views.ChangeRoleOnProjectView.as_view(),
        name='member-change-role'),

]