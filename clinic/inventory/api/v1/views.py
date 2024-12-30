from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from clinic.inventory.api.v1.serializers import SelectSupplySerializer, SupplySerializer
from clinic.inventory.filters import SupplyFilter
from clinic.inventory.models import Supply
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff


class SupplyViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = SupplyFilter
    search_fields = ["lot", "item", "invoice", "no", "description"]
    ordering_fields = ["created_at", "expires_at", "quantity", "unit_cost", "charge"]
    filter_field = "clinic"


class SelectSupplyViewSet(QuerysetFilteredMixin, generics.ListAPIView):
    queryset = Supply.objects.query_remains(remain__gt=0).order_by("expires_at")
    serializer_class = SelectSupplySerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = SupplyFilter
    search_fields = ["lot", "item", "invoice", "no", "description"]
    ordering_fields = ["created_at", "expires_at", "quantity", "unit_cost", "charge"]
    filter_field = "clinic"
