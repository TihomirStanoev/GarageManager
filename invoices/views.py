from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from accounts.decorators import group_required
from accounts.mixins import GroupFilterMixin
from invoices.models import Invoice
from repairs.models import Repair


class InvoiceListView(GroupFilterMixin, ListView):
    group_filter = ['Manager']
    model = Invoice
    template_name = 'invoices/invoice_list.html'
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
    slug_field = 'invoice_number'
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'
    extra_context = {
        'title': 'Invoice Details'
    }

    def get_object(self, queryset=None):
        if self.in_groups:
            return super().get_object(queryset=queryset)
        return super().get_object(queryset=Invoice.objects.filter(owner=self.request.user))





@group_required('Manager')
def create_invoice_view(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)

    if request.method == 'POST':
        repair.is_invoiced = True
        repair.save()
        Invoice.objects.create(repair=repair, owner=repair.car.owner)
        return redirect('repairs:repairs_list')

    return redirect('repairs:repairs_detail', pk=repair_pk)