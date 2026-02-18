from django.contrib import admin

from cars.models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'plate', 'year', 'engine_type')
    list_filter = ('brand', 'year', 'engine_type')
    search_fields = ('brand', 'model', 'plate', 'year', 'engine_type')
    ordering = ('brand', 'model')


