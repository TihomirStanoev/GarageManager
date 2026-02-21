from django.contrib import admin
from django.urls import path, include

from repairs import views

app_name = 'repairs'

parts_patterns = [
    path('', views.PartListView.as_view(), name='parts_list'),
    path('create/', views.CreatePartView.as_view(), name='parts_create'),
    path('<int:pk>/', views.PartDetail.as_view(), name='parts_detail'),
    path('<int:pk>/update/', views.UpdatePartView.as_view(), name='parts_update'),
    path('<int:pk>/delete/', views.DeletePartView.as_view(), name='parts_delete'),
]


urlpatterns = [
    path('parts/', include(parts_patterns)),
]
