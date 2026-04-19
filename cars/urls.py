from django.urls import path
from cars import views

app_name = 'cars'


urlpatterns = [
    path('', views.CarListView.as_view(), name='list'),
    path('create/', views.CreateCarView.as_view(), name='create'),
    path('<slug:plate>/', views.CarDetailView.as_view(), name='detail'),
    path('<slug:plate>/update/', views.UpdateCarView.as_view(), name='update'),
    path('<slug:plate>/delete/', views.DeleteCarView.as_view(), name='delete'),
    path('<slug:plate>/hard-delete/', views.HardDeleteCarView.as_view(), name='hard_delete'),
    path('<slug:plate>/restore/', views.CarRestoreView.as_view(), name='restore'),
]
