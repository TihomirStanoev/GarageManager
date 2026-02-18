from django.contrib import admin

from repairs.models import Invoice, Part, Repair, RepairPart


# Register your models here.
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'owner', 'total_amount')
    search_fields = ('invoice_number', 'repair__car__plate', 'owner__first_name', 'owner__last_name', 'owner__email', 'owner__phone_number')
    ordering = ('-created_at',)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('category',)


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('category', 'status')


@admin.register(RepairPart)
class RepairPartAdmin(admin.ModelAdmin):
    list_display = ('repair', 'part', 'quantity', 'price')
    search_fields = ('repair__car__plate', 'part__name')
    list_filter = ('part__category',)