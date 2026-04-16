from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from invoices.models import Invoice
from repairs.models import Repair
from repairs.serializers import RepairInvoiceSerializer
from repairs.choices import StatusChoice


class InvoiceBaseSerializer(serializers.ModelSerializer):
    repair = RepairInvoiceSerializer(read_only=True)
    repair_id = serializers.PrimaryKeyRelatedField(
        queryset=Repair.objects.all(),
        source='repair',
        write_only=True,
    )

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'repair_id', 'repair', 'owner', 'total_amount', 'created_at']
        read_only_fields = ['invoice_number', 'owner', 'total_amount', 'created_at']


    def validate(self, data):
        repair = data.get('repair')

        if repair.status != StatusChoice.COMPLETED:
            raise ValidationError('Cannot invoice a repair that is not yet completed.')

        return data