from django.urls import path
from invoices import views




app_name = 'invoices'


urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='invoices_list'),
    path('<int:repair_pk>/create/', views.create_invoice_view, name='invoices_create'),
    path('<slug:slug>/', views.InvoiceDetailView.as_view(), name='invoices_detail'),
]
