from django.contrib.auth import get_user_model
from rest_framework import serializers
from cars.models import Car
from cars.serializers import CarSerializer
from repairs.models import Repair, Part, RepairPart

UserModel = get_user_model()

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'name', 'description', 'category']



class RepairPartSerializer(serializers.ModelSerializer):
    part = PartSerializer()
    parts_price = serializers.ReadOnlyField()
    class Meta:
        model = RepairPart
        fields = ['id', 'part', 'quantity', 'price', 'parts_price']



class RepairBaseSerializer(serializers.ModelSerializer):
    assigned_mechanics = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(),
        many=True,
    )
    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
    )

    class Meta:
        model = Repair
        fields = ['id',
                  'category',
                  'description',
                  'status',
                  'labor_hours',
                  'price_per_labor_hour',
                  'car',
                  'assigned_mechanics',]




class RepairLimitedSerializer(RepairBaseSerializer):
    class Meta(RepairBaseSerializer.Meta):
        fields = ['id',
                  'category',
                  'description',
                  'status',
                  'car',]



class RepairInvoiceSerializer(RepairBaseSerializer):
    car = CarSerializer()
    part_entries = RepairPartSerializer(
        many=True,
        read_only=True
    )
    parts_price = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta(RepairBaseSerializer.Meta):
        fields = ['id',
                  'category',
                  'description',
                  'car',
                  'part_entries',
                  'assigned_mechanics',
                  'labor_hours',
                  'price_per_labor_hour',
                  'parts_price',
                  'total_price',
                  ]