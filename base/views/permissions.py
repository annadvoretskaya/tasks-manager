from django.core.exceptions import PermissionDenied


class PermissionsMixin(object):
    permission_classes = []

    def get_object(self, queryset=None):
        obj = super(PermissionsMixin, self).get_object(queryset)
        for permission in self.permission_classes:
            if not permission().has_permissions(self.request, obj):
                raise PermissionDenied
        return obj