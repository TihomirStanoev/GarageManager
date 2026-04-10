from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from cars.models import Car
from repairs.choices import StatusChoice
from repairs.forms import CreatePartForm, UpdatePartForm, CreateRepairForm, UpdateRepairForm, RepairPartForm, \
    CreateRepairWithCarForm
from repairs.models import Part, Repair, RepairPart, Invoice


class CreatePartView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = CreatePartForm
    template_name = 'repairs/parts/part_create.html'
    success_url = reverse_lazy('repairs:parts_list')
    extra_context = {
        'title': 'Create Part'
    }

class UpdatePartView(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = UpdatePartForm
    template_name = 'repairs/parts/part_update.html'
    success_url = reverse_lazy('repairs:parts_list')
    context_object_name = 'part'
    extra_context = {
        'title': 'Update Part'
    }


class DeletePartView(LoginRequiredMixin, DeleteView):
    model = Part
    template_name = 'repairs/parts/part_delete.html'
    success_url = reverse_lazy('repairs:parts_list')
    context_object_name = 'part'
    extra_context = {
        'title': 'Delete Part'
    }


class PartListView(LoginRequiredMixin, ListView):
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


class PartDetail(LoginRequiredMixin, DetailView):
    model = Part
    template_name = 'repairs/parts/part_detail.html'
    context_object_name = 'part'
    extra_context = {
        'title': 'Part Details'
    }


class RepairCreateView(LoginRequiredMixin, CreateView):
    model = Repair
    form_class = CreateRepairForm
    template_name = 'repairs/repairs/repair_create.html'
    success_url = reverse_lazy('repairs:repairs_list')
    extra_context = {
        'title': 'Create Repair'
    }


class RepairUpdateView(LoginRequiredMixin, UpdateView):
    model = Repair
    form_class = UpdateRepairForm
    template_name = 'repairs/repairs/repair_update.html'
    context_object_name = 'repair'
    extra_context = {
        'title': 'Update Repair'
    }

    def get_success_url(self):
        repair_pk = self.object.pk
        return reverse_lazy('repairs:repairs_detail', kwargs={'pk': repair_pk})



class RepairDeleteView(LoginRequiredMixin, DeleteView):
    model = Repair
    template_name = 'repairs/repairs/repair_delete.html'
    success_url = reverse_lazy('repairs:repairs_list')
    context_object_name = 'repair'
    extra_context = {
        'title': 'Delete Repair'
    }



class RepairListView(LoginRequiredMixin, ListView):
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
            case StatusChoice.IN_PROGRESS:
                repair.status = StatusChoice.COMPLETED

        repair.save()
        return redirect(reverse_lazy('repairs:repairs_list'))


    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Repair.objects.prefetch_related('parts').select_related('car').filter(is_invoiced=False).order_by('-status' , '-updated_at')

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


class RepairDetailView(LoginRequiredMixin, DetailView):
    model = Repair
    template_name = 'repairs/repairs/repair_detail.html'
    context_object_name = 'repair'
    extra_context = {
        'title': 'Repair Details'
    }


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'repairs/invoices/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 8
    extra_context = {
        'title': 'Invoices'
    }

    def get_queryset(self):
        queryset = Invoice.objects.select_related('repair', 'owner').order_by('-created_at')
        q = self.request.GET.get('q')

        if q:
            query = (Q(repair__car__plate__icontains=q) |
                     Q(repair__car__brand__icontains=q) |
                     Q(repair__car__owner__first_name__icontains=q) |
                     Q(repair__car__owner__last_name__icontains=q) |
                     Q(invoice_number=q))

            return queryset.filter(query)

        return queryset


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'repairs/invoices/invoice_detail.html'
    context_object_name = 'invoice'
    extra_context = {
        'title': 'Invoice Details'
    }


@login_required
def add_part_to_repair(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)
    category = repair.category

    form = RepairPartForm(request.POST or None, repair_category = category)

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





@login_required
def create_repair_with_car(request, car_plate):
    car = get_object_or_404(Car, plate=car_plate)
    form = CreateRepairWithCarForm(request.POST or None, initial={'car': car})
    context = {
        'form': form,
        'title': 'Create Repair',
    }

    if form.is_valid():
        repair = form.save(commit=False)
        repair.car = car
        repair.save()
        return redirect('repairs:repairs_detail', pk=repair.pk)

    return render(request, 'repairs/repairs/repair_create.html', context)



@login_required
def delete_part_from_repair(request, repair_pk, part_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)
    repair_part = get_object_or_404(RepairPart, pk=part_pk, repair=repair)


    if request.method == 'POST':
        repair_part.delete()
    return redirect('repairs:repairs_detail', pk=repair_pk)

@login_required
def create_invoice_view(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)

    if request.method == 'POST':
        repair.is_invoiced = True
        repair.save()
        Invoice.objects.create(repair=repair)
        return redirect('repairs:repairs_list')

    return redirect('repairs:repairs_detail', pk=repair_pk)

