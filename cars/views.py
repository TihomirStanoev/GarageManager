from django.db.migrations import DeleteModel
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from cars.forms import CreateCarForm, UpdateCarForm
from cars.models import Car





class CreateCarView(CreateView):
    model = Car
    form_class = CreateCarForm
    template_name = 'cars/car_create.html'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Create Car'
    }

class UpdateCarView(UpdateView):
    model = Car
    form_class = UpdateCarForm
    template_name = 'cars/car_update.html'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Update Car'
    }

class DeleteCar(DeleteView):
    model = Car
    template_name = 'cars/car_delete.html'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    success_url = reverse_lazy('cars:list')
    extra_context = {
        'title': 'Delete Car'
    }


class CarList(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 8
    extra_context = {
        'title': 'Cars'
    }

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            query = Q(plate__icontains=q) | Q(model__icontains=q)
            return Car.objects.prefetch_related('owner').filter(query)
        return Car.objects.prefetch_related('owner')


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_url_kwarg = 'plate'
    slug_field = 'plate'
    extra_context = {
        'title': 'Car Details'
    }