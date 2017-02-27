from rest_framework import permissions
from rest_framework import status
from rest_framework import views, viewsets, mixins

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from api import serializers
from api.permissions import IsProjectManager
from base.models import ApplicationUser, Project, Task, Invite


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = ApplicationUser.objects.all()
    serializer_class = serializers.UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsProjectManager]

    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    retrieve_serializer_class = serializers.RetrieveProjectSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return self.retrieve_serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NestedProjectMixinViewSet(viewsets.GenericViewSet):
    def initial(self, request, *args, **kwargs):
        super(NestedProjectMixinViewSet, self).initial(request, *args, **kwargs)
        project_pk = kwargs.get('project_pk')
        self.project = get_object_or_404(Project, pk=project_pk)


class TaskViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, NestedProjectMixinViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    retrieve_serializer_class = serializers.RetrieveTaskSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return self.retrieve_serializer_class
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(project=self.project)

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class InviteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, NestedProjectMixinViewSet):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.InviteSerializer
    queryset = Invite.objects.all()

    def get_queryset(self):
        return self.queryset.filter(project=self.project)

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class ProjectMembersViewSet(mixins.DestroyModelMixin, mixins.ListModelMixin, NestedProjectMixinViewSet):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.UserSerializer
    queryset = ApplicationUser.objects.all()

    def get_queryset(self):
        return self.queryset.filter(tasks__project=self.project).distinct()

    def perform_destroy(self, instance):
        self.project.remove_member(instance)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        token = request.user.auth_token
        if token:
            token.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
