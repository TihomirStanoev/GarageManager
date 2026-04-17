from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsMechanic, IsManager
from repairs.models import Part, Repair
from repairs.serializers import PartSerializer, RepairLimitedSerializer, RepairBaseSerializer


class PartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager | IsMechanic]
    queryset = Part.objects.all()
    serializer_class = PartSerializer



class RepairListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RepairLimitedSerializer

    def get_queryset(self):
        return Repair.objects.filter(car__owner = self.request.user)


class RepairManagerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = (Repair.objects.select_related('car')
                .prefetch_related('assigned_mechanics', 'parts'))
    serializer_class = RepairBaseSerializer




class RepairMechanicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsMechanic]
    serializer_class = RepairLimitedSerializer


    def get_queryset(self):
        return Repair.objects.filter(assigned_mechanics=self.request.user)
