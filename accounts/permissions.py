from rest_framework.permissions import BasePermission




class GroupPermission(BasePermission):
    group_required = []
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        return request.user.is_authenticated and any(group in user_groups for group in self.group_required)


class IsManager(GroupPermission):
    group_required = ['Manager']


class IsMechanic(GroupPermission):
    group_required = ['Mechanic']