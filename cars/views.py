from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from cars.forms import CreateCarForm
from cars.models import Car





class CreateCarView(CreateView):
    model = Car
    form_class = CreateCarForm
    template_name = 'cars/create_car.html'
    success_url = reverse_lazy('home:index')
    extra_context = {
        'title': 'Create Car'
    }



class CarList(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 10
    extra_context = {
        'title': 'Cars'
    }
