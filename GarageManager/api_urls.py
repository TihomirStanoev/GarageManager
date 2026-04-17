from django.urls import path, include




urlpatterns = [
    path('cars/', include('cars.api_urls')),
    path('repairs/', include('repairs.api_urls')),
    path('invoices/', include('invoices.api_urls')),
    path('token/', include('common.api_urls')),
]