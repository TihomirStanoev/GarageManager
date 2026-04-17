from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsManager
from invoices.models import Invoice
from invoices.serializers import InvoiceBaseSerializer




class InvoiceListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceBaseSerializer

    def get_queryset(self):
        return Invoice.objects.select_related('repair', 'owner').filter(owner = self.request.user)


class InvoiceDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceBaseSerializer

    def get_queryset(self):
        return Invoice.objects.select_related('repair', 'owner').filter(owner = self.request.user)

class InvoiceManagerAPIView(ListCreateAPIView):
    serializer_class = InvoiceBaseSerializer
    permission_classes = [IsManager]


    def get_queryset(self):
        return Invoice.objects.select_related('repair', 'owner')


