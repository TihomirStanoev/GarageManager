from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from accounts.mixins import GroupRequiredMixin, GroupFilterMixin
from cars.forms import CreateCarForm, UpdateCarForm
from cars.mixins import CarNotificationMixin
from cars.models import Car
from common.views import HardDeleteView, RestoreView


class CreateCarView(GroupRequiredMixin, CarNotificationMixin, CreateView):
    group_required = ['Manager']
    model = Car
    form_class = CreateCarForm
    template_name = 'cars/car_create.html'
    template_add_car_owner_subject = 'cars/emails/add_car_subject.txt'
    template_add_car_owner_message = 'cars/emails/add_car_message.txt'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Create Car'
    }


class UpdateCarView(GroupRequiredMixin, CarNotificationMixin, UpdateView):
    group_required = ['Manager']
    model = Car
    form_class = UpdateCarForm
    template_name = 'cars/car_update.html'
    template_add_car_owner_subject = 'cars/emails/add_car_subject.txt'
    template_add_car_owner_message = 'cars/emails/add_car_message.txt'
    template_remove_car_owner_subject = 'cars/emails/remove_car_subject.txt'
    template_remove_car_owner_message = 'cars/emails/remove_car_message.txt'

    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Update Car'
    }

class DeleteCarView(GroupRequiredMixin, DeleteView):
    group_required = ['Manager']
    model = Car
    template_name = 'cars/car_delete.html'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Delete Car'
    }


class HardDeleteCarView(HardDeleteView):
    model = Car
    success_url = reverse_lazy('cars:list')
    template_name = 'cars/car_hard_delete.html'
    context_object_name = 'car'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'



class CarRestoreView(RestoreView):
    model = Car
    success_url = reverse_lazy('cars:list')
    template_name = 'cars/car_restore.html'
    context_object_name = 'car'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'


class CarListView(GroupFilterMixin, ListView):
    group_filter = ['Manager', 'Mechanic']
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 8
    extra_context = {
        'title': 'Cars'
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Car.all_objects.select_related('owner')
        elif self.in_groups:
            queryset = Car.objects.select_related('owner')
        else:
            queryset = (Car.objects.select_related('owner')
                        .filter(owner=self.request.user))

        q = self.request.GET.get('q')
        if q:
            query = Q(plate__icontains=q) | Q(model__icontains=q)
            return queryset.filter(query)
        return queryset



class CarDetailView(GroupFilterMixin, DetailView):
    group_filter = ['Manager', 'Mechanic']
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    extra_context = {
        'title': 'Car Details'
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return Car.all_objects.all()
        if self.in_groups:
            return Car.objects.all()
        return Car.objects.filter(owner = self.request.user)



