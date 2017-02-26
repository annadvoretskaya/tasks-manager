from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from base.views import SignUpView, ProjectsListView, CreateProjectView, UpdateProjectView, DeleteProjectView, \
    ProjectDetailView, CreateInviteView, JoinProjectView, DetailTaskView, CreateTaskView, UpdateTaskView, \
    DeleteTaskView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='base:projects'), name='projects-redirect'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),

    url(r'^projects/$', ProjectsListView.as_view(), name='projects'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name='project-detail'),
    url(r'^projects/(?P<pk>\d+)/invite/$', CreateInviteView.as_view(), name='project-invite'),
    url(r'^projects/(?P<pk>\d+)/update/$', UpdateProjectView.as_view(), name='project-update'),
    url(r'^projects/(?P<pk>\d+)/delete/$', DeleteProjectView.as_view(), name='project-delete'),
    url(r'^projects/new/$', CreateProjectView.as_view(), name='project-create'),
    url(r'^join/(?P<pk>[\w-]+)/$', JoinProjectView.as_view(), name='project-join'),

    url(r'^projects/(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/$', DetailTaskView.as_view(), name='task-detail'),
    url(r'^projects/(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/update/$', UpdateTaskView.as_view(), name='task-update'),
    url(r'^projects/(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/delete/$', DeleteTaskView.as_view(), name='task-delete'),
    url(r'^projects/(?P<project_pk>\d+)/tasks/new/$', CreateTaskView.as_view(), name='task-create'),

]