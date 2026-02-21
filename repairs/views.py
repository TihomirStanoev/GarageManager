from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from repairs.forms import CreatePartForm, UpdatePartForm
from repairs.models import Part


class CreatePartView(CreateView):
    model = Part
    form_class = CreatePartForm
    template_name = 'repairs/parts/part_create.html'
    success_url = reverse_lazy('home:index')
    extra_context = {
        'title': 'Create Part'
    }

class UpdatePartView(UpdateView):
    model = Part
    form_class = UpdatePartForm
    template_name = 'repairs/parts/part_update.html'
    success_url = reverse_lazy('repairs:parts_list')
    context_object_name = 'part'
    extra_context = {
        'title': 'Update Part'
    }


class DeletePartView(DeleteView):
    model = Part
    template_name = 'repairs/parts/part_delete.html'
    success_url = reverse_lazy('repairs:parts_list')
    context_object_name = 'part'
    extra_context = {
        'title': 'Delete Part'
    }




class PartListView(ListView):
    model = Part
    template_name = 'repairs/parts/part_list.html'
    context_object_name = 'parts'
    paginate_by = 8
    extra_context = {
        'title': 'Parts'
    }

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            query = Q(name__icontains=q) | Q(description__icontains=q)
            return Part.objects.filter(query)
        return Part.objects.all()


class PartDetail(DetailView):
    model = Part
    template_name = 'repairs/parts/part_detail.html'
    context_object_name = 'part'
    extra_context = {
        'title': 'Part Details'
    }
