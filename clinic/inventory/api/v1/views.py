from rest_framework import generics, viewsets

from clinic.inventory.api.v1.serializers import SelectSupplySerializer, SupplySerializer
from clinic.inventory.filters import SelectSupplyFilter, SupplyFilter
from clinic.inventory.models import Supply
from clinic.users.api.permissions import IsAdminStaff, IsStaff


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    filterset_class = SupplyFilter
    permission_classes = [IsAdminStaff]


class SelectSupplyViewSet(generics.ListAPIView):
    queryset = Supply.objects.all()
    serializer_class = SelectSupplySerializer
    filterset_class = SelectSupplyFilter
    permission_classes = [IsStaff]
