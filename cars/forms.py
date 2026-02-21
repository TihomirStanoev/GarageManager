from django import forms

from cars.models import Car


class BaseCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'plate', 'engine_type', 'mileage', 'image', 'owner']

        widgets = {
            'brand': forms.Select,
            'model': forms.TextInput(attrs={'placeholder': '320i/Civic'}),
            'year': forms.NumberInput(attrs={'placeholder': '1999'}),
            'plate': forms.TextInput(attrs={'placeholder': 'CB1234CB', 'text-transform': 'uppercase'}),
            'engine_type': forms.Select,
            'mileage': forms.NumberInput(attrs={'placeholder': '120000'}),
            'owner': forms.Select,
        }

        labels = {
            'brand': 'Brand',
            'model': 'Model',
            'year': 'Year',
            'plate': 'Plate',
            'engine_type': 'Engine Type',
            'mileage': 'Mileage',
            'image': 'Image',
            'owner': 'Owner',
        }

        help_texts = {
            'brand': 'Select a brand',
            'model': 'Enter a model',
            'year': 'Enter a year',
            'plate': 'Enter a plate',
        }

        error_messages = {
            'plate': {
                'unique': 'A car with this plate already exists.'
            },
            'year': {
                'invalid': 'Enter a valid year.'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'owner' in self.fields:
            self.fields['owner'].label_from_instance = lambda p: p.profile_with_phone


class CreateCarForm(BaseCarForm):
    pass


class UpdateCarForm(BaseCarForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        disabled_fields = {'brand', 'year', 'plate', 'engine_type', 'mileage'}
        for field in disabled_fields:
            self.fields[field].disabled = True



