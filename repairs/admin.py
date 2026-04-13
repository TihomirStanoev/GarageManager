from django.contrib import admin

from repairs.models import Part, Repair, RepairPart


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