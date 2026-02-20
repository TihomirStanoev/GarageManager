from django.shortcuts import render
from django.views.generic import TemplateView

from profiles.models import Profile


class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'title': 'Home'
    }

    def get_context_data(self, **kwargs):
        kwargs['total_clients'] = Profile.objects.count()

        return super().get_context_data(**kwargs)

