from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from clinic.healthcare.api.v1.serializers import SelectServiceSerializer, ServiceSerializer
from clinic.healthcare.filters import ServiceFilter
from clinic.healthcare.models import Service
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff


class ServiceViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ServiceFilter
    search_fields = ["name", "description"]
    ordering_fields = ["created_at"]
    filter_field = "clinic"


class SelectServiceView(QuerysetFilteredMixin, generics.ListAPIView):
    """
    API endpoint that allows services to be viewed as list.
    """

    queryset = Service.objects.get_queryset().filter(active=True)
    serializer_class = SelectServiceSerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at"]
    filter_field = "clinic"
