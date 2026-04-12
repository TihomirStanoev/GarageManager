from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, DetailView, UpdateView
from accounts.decorators import group_required
from accounts.forms import RegisterForm, LoginForm, UpdateProfileForm
from accounts.mixins import GroupFilterMixin



UserModel = get_user_model()

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


class ProfileDetailView(GroupFilterMixin, DetailView):
    group_filter = ['Manager']
    model = UserModel
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'user'
    extra_context = {
        'title': 'User Profile'
    }

    def get_object(self, queryset = None):
        if not self.in_groups:
            queryset = UserModel.objects.filter(pk=self.request.user.pk)
        return super().get_object(queryset)



class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'accounts/profile_update.html'
    form_class = UpdateProfileForm


    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset = None):
        return self.request.user



@group_required('Manager')
def toggle_active(request, pk):
    user = get_object_or_404(UserModel, pk=pk)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()

    return redirect('accounts:profile', pk=pk)




