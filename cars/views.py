from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from accounts.mixins import GroupRequiredMixin, GroupFilterMixin
from cars.forms import CreateCarForm, UpdateCarForm
from cars.models import Car





class CreateCarView(GroupRequiredMixin, CreateView):
    group_required = ['Manager']
    model = Car
    form_class = CreateCarForm
    template_name = 'cars/car_create.html'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Create Car'
    }

class UpdateCarView(GroupRequiredMixin, UpdateView):
    group_required = ['Manager']
    model = Car
    form_class = UpdateCarForm
    template_name = 'cars/car_update.html'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Update Car'
    }

class DeleteCar(GroupRequiredMixin, DeleteView):
    group_required = ['Manager']
    model = Car
    template_name = 'cars/car_delete.html'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Delete Car'
    }


class CarList(GroupFilterMixin, ListView):
    group_filter = ['Manager', 'Mechanic']
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 8
    extra_context = {
        'title': 'Cars'
    }

    def get_queryset(self):
        queryset = Car.objects.select_related('owner')
        q = self.request.GET.get('q')


        if not self.in_groups:
            query = Q(owner__pk=self.request.user.pk)
            queryset = queryset.filter(query)

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
        if self.in_groups:
            return Car.objects.all()
        return Car.objects.filter(owner = self.request.user)