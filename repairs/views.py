from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from accounts.decorators import group_required
from accounts.mixins import GroupRequiredMixin, GroupFilterMixin
from cars.models import Car
from repairs.choices import StatusChoice
from repairs.forms import CreatePartForm, UpdatePartForm, CreateRepairForm, UpdateRepairForm, RepairPartForm, \
    CreateRepairWithCarForm
from repairs.models import Part, Repair, RepairPart, Invoice


class CreatePartView(GroupRequiredMixin, CreateView):
    group_required = ['Mechanic', 'Manager']
    model = Part
    form_class = CreatePartForm
    template_name = 'repairs/parts/part_create.html'
    success_url = reverse_lazy('repairs:parts_list')
    extra_context = {
        'title': 'Create Part'
    }

class UpdatePartView(GroupRequiredMixin, UpdateView):
    group_required = ['Mechanic', 'Manager']
    model = Part
    form_class = UpdatePartForm
    template_name = 'repairs/parts/part_update.html'
    success_url = reverse_lazy('repairs:parts_list')
    context_object_name = 'part'
    extra_context = {
        'title': 'Update Part'
    }


class DeletePartView(GroupRequiredMixin, DeleteView):
    group_required = ['Manager']
    model = Part
    template_name = 'repairs/parts/part_delete.html'
    success_url = reverse_lazy('repairs:parts_list')
    context_object_name = 'part'
    extra_context = {
        'title': 'Delete Part'
    }


class PartListView(GroupRequiredMixin, ListView):
    group_required = ['Mechanic', 'Manager']
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


class PartDetail(GroupRequiredMixin, DetailView):
    group_required = ['Mechanic', 'Manager']
    model = Part
    template_name = 'repairs/parts/part_detail.html'
    context_object_name = 'part'
    extra_context = {
        'title': 'Part Details'
    }


class RepairCreateView(GroupRequiredMixin, CreateView):
    group_required = ['Mechanic', 'Manager']
    model = Repair
    form_class = CreateRepairForm
    template_name = 'repairs/repairs/repair_create.html'
    success_url = reverse_lazy('repairs:repairs_list')
    extra_context = {
        'title': 'Create Repair'
    }


class RepairUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ['Manager']
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



class RepairDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ['Manager']
    model = Repair
    template_name = 'repairs/repairs/repair_delete.html'
    success_url = reverse_lazy('repairs:repairs_list')
    context_object_name = 'repair'
    extra_context = {
        'title': 'Delete Repair'
    }



class RepairListView(GroupFilterMixin, ListView):
    group_filter = ['Mechanic', 'Manager']
    model = Repair
    template_name = 'repairs/repairs/repair_list.html'
    context_object_name = 'repairs'
    paginate_by = 8
    extra_context = {
        'title': 'Repairs'
    }

    def post(self, request, *args, **kwargs):
        repair_id = request.POST.get('repair_id')
        repair = get_object_or_404(Repair, pk=repair_id)
        status = repair.status

        match status:
            case StatusChoice.DRAFT:
                repair.status = StatusChoice.IN_PROGRESS
            case StatusChoice.IN_PROGRESS:
                if repair.assigned_mechanics.all():
                    repair.status = StatusChoice.COMPLETED

        if repair.status != status:
            repair.save()

        return redirect(reverse_lazy('repairs:repairs_list'))


    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = (Repair.objects.prefetch_related('parts', 'assigned_mechanics').select_related('car').
                    filter(is_invoiced=False).
                    order_by('-status' , '-updated_at'))

        if not self.in_groups:
            queryset = queryset.filter(car__owner=self.request.user)

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
        context['is_mechanic'] = 'Mechanic' in self.request.user.groups.values_list('name', flat=True)
        context['is_manager'] = 'Manager' in self.request.user.groups.values_list('name', flat=True)
        return context


class RepairDetailView(GroupFilterMixin, DetailView):
    group_filter = ['Mechanic', 'Manager']
    model = Repair
    template_name = 'repairs/repairs/repair_detail.html'
    context_object_name = 'repair'
    extra_context = {
        'title': 'Repair Details'
    }

    def get_queryset(self):
        if self.in_groups:
            return Repair.objects.all()
        return Repair.objects.filter(car__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_manager'] = 'Manager' in self.request.user.groups.values_list('name', flat=True)

        return context


class InvoiceListView(GroupFilterMixin, ListView):
    group_filter = ['Manager']
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

        if not self.in_groups:
            queryset = queryset.filter(owner=self.request.user)

        if q:
            query = (Q(repair__car__plate__icontains=q) |
                     Q(repair__car__brand__icontains=q) |
                     Q(repair__car__owner__first_name__icontains=q) |
                     Q(repair__car__owner__last_name__icontains=q) |
                     Q(invoice_number=q))

            return queryset.filter(query)

        return queryset


class InvoiceDetailView(GroupFilterMixin, DetailView):
    group_filter = ['Manager']
    model = Invoice
    template_name = 'repairs/invoices/invoice_detail.html'
    context_object_name = 'invoice'
    extra_context = {
        'title': 'Invoice Details'
    }

    def get_object(self, queryset=None):
        if self.in_groups:
            return super().get_object(queryset=queryset)
        return super().get_object(queryset=Invoice.objects.filter(owner=self.request.user))


@group_required('Mechanic', 'Manager')
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





@group_required('Mechanic', 'Manager')
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



@group_required('Mechanic', 'Manager')
def delete_part_from_repair(request, repair_pk, part_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)
    repair_part = get_object_or_404(RepairPart, pk=part_pk, repair=repair)


    if request.method == 'POST':
        repair_part.delete()
    return redirect('repairs:repairs_detail', pk=repair_pk)

@group_required('Manager')
def create_invoice_view(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)

    if request.method == 'POST':
        repair.is_invoiced = True
        repair.save()
        Invoice.objects.create(repair=repair)
        return redirect('repairs:repairs_list')

    return redirect('repairs:repairs_detail', pk=repair_pk)


@group_required('Mechanic')
def assign_unassign_repair_to_mechanic(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)

    if request.method == 'POST' and repair.status != StatusChoice.COMPLETED:
        mechanic = request.user
        repair_mechanics = repair.assigned_mechanics.all()

        if mechanic not in repair_mechanics:
            repair.assigned_mechanics.add(mechanic)
        else:
            repair.assigned_mechanics.remove(mechanic)

    return redirect('repairs:repairs_list')
