from django.contrib.auth import get_user_model
import django.contrib.auth.forms as auth_forms

User = get_user_model()

class RegisterForm(auth_forms.BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number')



class LoginForm(auth_forms.AuthenticationForm):
    pass


class UpdateProfileForm(auth_forms.UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'last_login')




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ('email', 'last_login'):
            self.fields[field].disabled = True





