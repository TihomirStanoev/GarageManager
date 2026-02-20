from django import forms

from profiles.models import Profile


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ivan'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ivanov'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+359888123456'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ivan@garage.com'}),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone',
            'email': 'Email',
        }

        help_texts = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'phone_number': 'Enter your phone number',
            'email': 'Enter your email',
        }

        error_messages = {
            'email': {
                'unique': 'A client with this email already exists.'
            },
            'phone_number': {
                'unique': 'A client with this phone number already exists.'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name:
            cleaned_data['first_name'] = first_name.capitalize()
        if last_name:
            cleaned_data['last_name'] = last_name.capitalize()

        return cleaned_data




class CreateProfileForm(BaseProfileForm):
    pass





class UpdateProfileForm(BaseProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True




