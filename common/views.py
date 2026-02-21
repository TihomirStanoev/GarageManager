from django.shortcuts import render
from django.views.generic import TemplateView

from cars.models import Car
from profiles.models import Profile
from repairs.choices import StatusChoice
from repairs.models import Part, Repair


class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'title': 'Home'
    }

    def get_context_data(self, **kwargs):
        kwargs['total_clients'] = Profile.objects.count()
        kwargs['total_cars'] = Car.objects.count()
        kwargs['total_parts'] = Part.objects.count()
        kwargs['total_repairs'] = Repair.objects.filter(status=StatusChoice.DRAFT).count()

        return super().get_context_data(**kwargs)

