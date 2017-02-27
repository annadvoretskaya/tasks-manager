from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from rest_framework_nested.routers import NestedSimpleRouter

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet)

tasks_router = NestedSimpleRouter(router, r'projects', lookup='project')
tasks_router.register(r'tasks', views.TaskViewSet)

invites_router = NestedSimpleRouter(router, r'projects', lookup='project')
invites_router.register(r'invites', views.InviteViewSet)

members_router = NestedSimpleRouter(router, r'projects', lookup='project')
members_router.register(r'members', views.ProjectMembersViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(tasks_router.urls)),
    url(r'^', include(invites_router.urls)),
    url(r'^', include(members_router.urls)),
    url(r'^login/?', auth_views.obtain_auth_token, name="login"),
    url(r'^logout/?', views.LogoutView.as_view(), name="logout"),
]