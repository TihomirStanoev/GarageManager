from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, DetailView, UpdateView, ListView
from accounts.decorators import group_required
from accounts.forms import RegisterForm, LoginForm, UpdateProfileForm
from accounts.mixins import GroupFilterMixin, GroupRequiredMixin

UserModel = get_user_model()

class ProfileRegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='accounts.backends.EmailBackend')
        return super().form_valid(form)


class ProfileLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class ProfileLogoutView(LogoutView):
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



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'accounts/profile_update.html'
    form_class = UpdateProfileForm
    extra_context = {
        'title': 'Change Profile'
    }


    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset = None):
        return self.request.user




class ProfileListView(GroupRequiredMixin, ListView):
    group_required = ['Manager']
    model = UserModel
    context_object_name = 'users'
    template_name = 'accounts/profile_list.html'
    paginate_by = 8
    extra_context = {
        'title': 'List Profiles'
    }

    def get_queryset(self):
        queryset = UserModel.objects.prefetch_related('cars', 'invoices')
        q = self.request.GET.get('q')

        if q:
            query = Q(first_name__icontains=q) | Q(last_name__icontains=q)
            return queryset.filter(query)
        return queryset


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = self.object_list.count()

        return context




@group_required('Manager')
def toggle_active(request, pk):
    user = get_object_or_404(UserModel, pk=pk)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()

    return redirect('accounts:profile', pk=pk)


@group_required('Manager')
def toggle_role(request, pk):
    user = get_object_or_404(UserModel, pk=pk)

    if request.method == 'POST':
        role = request.POST.get('role')
        group = get_object_or_404(Group, name=role)

        if not user.groups.filter(pk=group.pk).exists():
            user.groups.add(group)
        else:
            user.groups.remove(group)


    return redirect('accounts:profile', pk=pk)
