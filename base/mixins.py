from django.core.exceptions import PermissionDenied


class ProjectsByUserMixin(object):
    def get_queryset(self):
        queryset = super(ProjectsByUserMixin, self).get_queryset()
        return queryset.by_user(self.request.user)


class ProjectTasksMixin(object):
    def get_queryset(self):
        queryset = super(ProjectTasksMixin, self).get_queryset()
        project_id = self.kwargs.get('project_pk', None)
        return queryset.filter(project_id=project_id)


class PermissionsMixin(object):
    permission_classes = []

    def get_object(self, queryset=None):
        obj = super(PermissionsMixin, self).get_object(queryset)
        for permission in self.permission_classes:
            if not permission().has_permissions(self.request, obj):
                raise PermissionDenied
        return obj
