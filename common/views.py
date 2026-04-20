from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from cars.models import Car
from common.service import hard_delete_object, restore_object
from invoices.models import Invoice
from repairs.choices import StatusChoice
from repairs.models import Part, Repair
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.detail import SingleObjectMixin



User = get_user_model()

class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'title': 'Home'
    }

    def get_context_data(self, **kwargs):
        kwargs['total_clients'] = User.objects.count()
        kwargs['total_cars'] = Car.objects.count()
        kwargs['total_parts'] = Part.objects.count()
        kwargs['total_repairs'] = Repair.objects.filter(status__in=[StatusChoice.DRAFT, StatusChoice.IN_PROGRESS]).count()
        kwargs['total_invoices'] = Invoice.objects.count()

        return super().get_context_data(**kwargs)

class SoftDeletionBaseView(LoginRequiredMixin, UserPassesTestMixin, SingleObjectMixin, View):
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

class RestoreView(SoftDeletionBaseView):
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        restore_object(obj, request.user)
        return super().post(request, *args, **kwargs)



class HardDeleteView(SoftDeletionBaseView):
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        hard_delete_object(obj, request.user)
        return super().post(request, *args, **kwargs)
