from django.contrib import admin

from invoices.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'owner', 'total_amount')
    search_fields = ('invoice_number', 'repair__car__plate', 'owner__first_name', 'owner__last_name', 'owner__email', 'owner__phone_number')
    ordering = ('-created_at',)
