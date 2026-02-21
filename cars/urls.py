from django.urls import path
from cars import views

app_name = 'cars'


urlpatterns = [
    path('', views.CarList.as_view(), name='list'),
    path('create/', views.CreateCarView.as_view(), name='create'),
    path('<slug:plate>/', views.CarDetailView.as_view(), name='detail'),
    path('<slug:plate>/update/', views.UpdateCarView.as_view(), name='update'),
    path('<slug:plate>/delete/', views.DeleteCar.as_view(), name='delete'),
]
