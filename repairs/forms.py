from django import forms

from common.models import RepairPartMixin
from repairs.models import Part


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
