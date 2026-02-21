from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from repairs.choices import StatusChoice
from repairs.forms import CreatePartForm, UpdatePartForm, CreateRepairForm, UpdateRepairForm, RepairPartForm
from repairs.models import Part, Repair


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


class RepairCreateView(CreateView):
    model = Repair
    form_class = CreateRepairForm
    template_name = 'repairs/repairs/repair_create.html'
    success_url = reverse_lazy('repairs:repairs_list')
    extra_context = {
        'title': 'Create Repair'
    }


class RepairUpdateView(UpdateView):
    model = Repair
    form_class = UpdateRepairForm
    template_name = 'repairs/repairs/repair_update.html'
    success_url = reverse_lazy('repairs:repairs_list')
    context_object_name = 'repair'
    extra_context = {
        'title': 'Update Repair'
    }




class RepairListView(ListView):
    model = Repair
    template_name = 'repairs/repairs/repair_list.html'
    context_object_name = 'repairs'
    paginate_by = 8
    extra_context = {
        'title': 'Repairs'
    }

    def post(self, request, *args, **kwargs):
        repair_id = request.POST.get('repair_id')
        repair = Repair.objects.get(pk=repair_id)

        match repair.status:
            case StatusChoice.DRAFT:
                repair.status = StatusChoice.IN_PROGRESS

        repair.save()
        return redirect(reverse_lazy('repairs:repairs_list'))


    def get_queryset(self):
        queryset = Repair.objects.prefetch_related('parts').select_related('car').order_by('-status')
        q = self.request.GET.get('q')
        if q:
            query = Q(car__plate__icontains=q) | Q(car__owner__first_name__icontains=q) | Q(car__owner__last_name__icontains=q)
            return queryset.filter(query)
        return  queryset


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        context['active_count'] = qs.filter(status=StatusChoice.IN_PROGRESS).count()
        context['completed_count'] = qs.filter(status=StatusChoice.COMPLETED).count()
        context['drafted_count'] = qs.filter(status=StatusChoice.DRAFT).count()
        context['cancelled_count'] = qs.filter(status=StatusChoice.CANCELLED).count()
        return context


class RepairDetailView(DetailView):
    model = Repair
    template_name = 'repairs/repairs/repair_detail.html'
    context_object_name = 'repair'
    extra_context = {
        'title': 'Repair Details'
    }


def add_part_to_repair(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)
    form = RepairPartForm(request.POST or None)


    if form.is_valid():
        try:
            repair_part = form.save(commit=False)
            repair_part.repair = repair
            repair_part.save()
            return redirect('repairs:repairs_detail', pk=repair_pk)
        except IntegrityError:
            form.add_error('part', 'This part has already been added to this repair.')

    context = {
        'form': form,
        'repair': repair,
        'title': 'Add Part to Repair',
    }

    return render(request, 'repairs/repairs/repair_add_part.html', context)



