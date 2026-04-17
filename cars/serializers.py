from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.serializers import AccountsSerializer
from cars.models import Car


UserModel = get_user_model()


class CarBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'plate', 'year', 'engine_type', 'mileage', 'owner']




class CarViewSetSerializer(CarBaseSerializer):
    owner = AccountsSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(),
        source='owner',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta(CarBaseSerializer.Meta):
        fields =  CarBaseSerializer.Meta.fields + ['owner_id']




class CarSerializer(CarBaseSerializer):
    pass
