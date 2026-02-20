from django.urls import path
from cars import views

app_name = 'cars'


urlpatterns = [
    path('', views.CarList.as_view(), name='list'),
    path('create/', views.CreateCarView.as_view(), name='create'),
]
