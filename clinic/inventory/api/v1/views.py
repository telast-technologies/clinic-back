from rest_framework import viewsets

from clinic.inventory.api.v1.serializers import SupplySerializer
from clinic.inventory.filters import SupplyFilter
from clinic.inventory.models import Supply
from clinic.users.api.permissions import IsAdminStaff


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    filterset_class = SupplyFilter
    permission_classes = [IsAdminStaff]
