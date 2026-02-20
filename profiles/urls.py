from django.contrib import admin
from django.urls import path

from profiles import views

app_name = 'profiles'


urlpatterns = [
    path('', views.ProfileList.as_view(), name='list'),

    path('create/', views.CreateProfileView.as_view(), name='create'),
    path('<int:pk>/', views.ProfileDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdateProfileView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteProfile.as_view(), name='delete'),

]
