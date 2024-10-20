from rest_framework import generics, viewsets

from clinic.healthcare.api.v1.serializers import SelectServiceSerializer, ServiceSerializer
from clinic.healthcare.filters import SelectServiceFilter, ServiceFilter
from clinic.healthcare.models import Service
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff, IsStaff


class ServiceViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_class = ServiceFilter
    permission_classes = [IsAdminStaff]
    filter_field = "clinic"


class SelectServiceView(QuerysetFilteredMixin, generics.ListAPIView):
    """
    API endpoint that allows services to be viewed as list.
    """

    queryset = Service.objects.get_queryset().filter(active=True)
    serializer_class = SelectServiceSerializer
    filterset_class = SelectServiceFilter
    permission_classes = [IsStaff]
    filter_field = "clinic"
