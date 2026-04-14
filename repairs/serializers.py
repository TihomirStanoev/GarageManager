from rest_framework import serializers

from repairs.models import Repair


class RepairSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['id', ]