
class BasePermission(object):
    def has_permissions(self, request, obj):
        raise NotImplementedError


class IsProjectOwnerPermission(BasePermission):
    def has_permissions(self, request, obj):
        return obj.is_owner(request.user)


class IsProjectOwnerOrManagerPermission(BasePermission):
    def has_permissions(self, request, obj):
        return obj.is_manager(request.user)


class IsTaskOwnerOrManagerPermission(BasePermission):
    def has_permissions(self, request, obj):
        return obj.project.is_manager(request.user)
