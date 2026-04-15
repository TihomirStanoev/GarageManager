from django.contrib.auth import get_user_model
from rest_framework import serializers
from cars.models import Car
from repairs.models import Repair, Part




UserModel = get_user_model()

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'name', 'description', 'category']




class RepairBaseSerializer(serializers.ModelSerializer):
    parts = serializers.PrimaryKeyRelatedField(
        queryset=Part.objects.all(),
        many=True
    )
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
                  'parts',
                  'assigned_mechanics',]





class RepairLimitedSerializer(RepairBaseSerializer):
    class Meta(RepairBaseSerializer.Meta):
        fields = ['id',
                  'category',
                  'description',
                  'status',
                  'car',
                  'parts',]