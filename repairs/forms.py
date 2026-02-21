from django import forms

from cars.models import Car
from common.models import RepairPartMixin
from repairs.models import Part, Repair, RepairPart


class BasePartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['category', 'name', 'description', 'image']
        widgets = {
            'category': forms.Select,
            'name': forms.TextInput(attrs={'placeholder': 'Control Arm'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description...', 'col':5, 'row':3}),
            'image': forms.FileInput
        }

        labels = {
            'category': 'Category',
            'name': 'Name',
            'description': 'Description',
            'image': 'Image'
        }

        error_messages = {
            'name': {
                'unique': 'A part with this name already exists.'
            }
        }


    def __init__(self, *args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = RepairPartMixin.CategoryChoice.OTHER



class CreatePartForm(BasePartForm):
    pass


class UpdatePartForm(BasePartForm):
    class Meta(BasePartForm.Meta):
        exclude = ['name']




class BaseRepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['category', 'description', 'labor_hours', 'price_per_labor_hour', 'status','car']

        widgets = {
            'category': forms.Select,
            'description': forms.Textarea(attrs={'placeholder': 'Description...', 'col':5, 'row':3}),
            'labor_hours': forms.NumberInput(attrs={'placeholder': '0.0'}),
            'price_per_labor_hour': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'status': forms.Select,
            'car': forms.Select,
        }

        labels = {
            'category': 'Category',
            'description': 'Description',
            'labor_hours': 'Labor Hours',
            'price_per_labor_hour': 'Hourly Rate',
            'status': 'Status',
            'car': 'Car',
            'parts': 'Parts'
        }

        error_messages = {
            'labor_hours': {
                'min_value': 'Labor hours cannot be negative.'
            },
            'price_per_labor_hour': {
                'min_value': 'Hourly rate cannot be negative.'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = RepairPartMixin.CategoryChoice.OTHER


class CreateRepairForm(BaseRepairForm):
    class Meta(BaseRepairForm.Meta):
        exclude = ['status', 'parts', 'labor_hours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.select_related('owner').filter(owner__isnull=False)




class UpdateRepairForm(BaseRepairForm):
    class Meta(BaseRepairForm.Meta):
        exclude = ['car']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].disabled = True


class RepairPartForm(forms.ModelForm):
    class Meta:
        model = RepairPart
        fields = ['part', 'quantity', 'price']

