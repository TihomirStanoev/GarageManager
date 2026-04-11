from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_groups = set(request.user.groups.values_list('name', flat=True))
        if not user_groups.intersection(self.allowed_roles):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Manager']


class MechanicRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['Mechanic']