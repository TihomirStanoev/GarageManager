from django.db.models import Q
from django.shortcuts import render
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView, ListView, DetailView, DeleteView

from profiles.forms import CreateProfileForm, UpdateProfileForm
from profiles.models import Profile



class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'profiles/profile_create.html'
    success_url = reverse_lazy('home:index')
    extra_context = {
        'title': 'Create Profile'
    }


class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('profiles:list')
    context_object_name = 'profile'
    extra_context = {
        'title': 'Update Profile'
    }


class DeleteProfile(DeleteView):
    model = Profile
    template_name = 'profiles/profile_delete.html'
    success_url = reverse_lazy('profiles:list')
    context_object_name = 'profile'
    extra_context = {
        'title': 'Delete Profile'
    }


class ProfileList(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 10
    extra_context = {
        'title': 'Clients'
    }




    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            query = Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(phone_number__icontains=q)
            return Profile.objects.prefetch_related('cars').filter(query)
        return Profile.objects.prefetch_related('cars')



class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    extra_context = {
        'title': 'Client Details'
    }
