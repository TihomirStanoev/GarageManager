from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsManager
from cars.models import Car
from cars.serializers import CarViewSetSerializer, CarSerializer



class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related('owner')
    serializer_class = CarViewSetSerializer
    permission_classes = [IsManager]



class UserCarListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get_queryset(self):
        owner = self.request.user
        return Car.objects.filter(owner=owner)




