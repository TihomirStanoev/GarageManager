from django import forms
from django.contrib.auth import get_user_model
import django.contrib.auth.forms as auth_forms

User = get_user_model()

class RegisterForm(auth_forms.BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number')



class LoginForm(auth_forms.AuthenticationForm):
    pass