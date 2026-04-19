from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.detail import SingleObjectMixin


class SoftDeletionMixin(LoginRequiredMixin, UserPassesTestMixin, SingleObjectMixin, View):
    model = None
    success_url = None
    template_name = None
    context_object_name = 'object'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return render(request, self.template_name, {self.context_object_name: obj})

    def get_queryset(self):
        return self.model.all_objects.all()