from django.urls import path
from invoices import api_views




urlpatterns = [
    path('my-invoices/', api_views.InvoiceListAPIView.as_view(), name='invoices_my_invoices'),
    path('my-invoices/<int:pk>/', api_views.InvoiceDetailAPIView.as_view(), name='invoices_my_invoices'),
    path('', api_views.InvoiceManagerAPIView.as_view(), name='invoice_manager'),

]