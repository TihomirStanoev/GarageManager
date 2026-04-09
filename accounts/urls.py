from django.urls import path
from accounts import views


app_name = 'accounts'


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.GarageLoginView.as_view(), name='login'),
    path('logout/', views.GarageLogoutView.as_view(), name='logout'),
]