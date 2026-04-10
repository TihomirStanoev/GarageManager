from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import RegisterForm, LoginForm





class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='accounts.backends.EmailBackend')
        return super().form_valid(form)


class GarageLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class GarageLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'
