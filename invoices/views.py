from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from common.tasks import send_mail_async
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
    group_filter = ['Manager', 'Mechanic']
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
        if not repair.labor_hours or not repair.price_per_labor_hour:
            messages.error(request, 'Cannot create invoice: labor hours and price per labor hour must be filled in. Use "Update Status and Hours" to fill them in.')
            return redirect('repairs:repairs_detail', pk=repair_pk)


        repair.is_invoiced = True
        repair.save()
        invoice = Invoice.objects.create(repair=repair, owner=repair.car.owner)

        context = {
            'car_plate': invoice.repair.car.plate,
            'owner_name': invoice.owner.first_name,
            'invoice_number': invoice.invoice_number,
            'total_amount': invoice.total_amount,
        }

        subject = render_to_string('invoices/email/notification_subject.txt', context)
        message = render_to_string('invoices/email/notification_message.txt', context)
        recipient = [invoice.owner.email]

        send_mail_async.delay(
            subject=subject,
            message=message,
            recipient_list=recipient
        )

        return redirect('invoices:invoices_detail', slug=invoice.invoice_number)

    return redirect('repairs:repairs_detail', pk=repair_pk)