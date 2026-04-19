from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin


class GroupRequiredMixin(AccessMixin):
    group_required = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()


        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        user_groups = request.user.groups.values_list('name', flat=True)
        if not any(group in user_groups for group in self.group_required):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)



class GroupFilterMixin(LoginRequiredMixin):
    group_filter = []

    @property
    def in_groups(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return any(g in user_groups for g in self.group_filter)


