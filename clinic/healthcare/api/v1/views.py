from rest_framework import generics, viewsets

from clinic.healthcare.api.v1.serializers import ServiceListSelectSerializer, ServiceSerializer
from clinic.healthcare.filters import ServiceFilter, ServiceListFilter
from clinic.healthcare.models import Service
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff, IsStaff


class ServiceViewset(QuerysetFilteredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_class = ServiceFilter
    permission_classes = [IsAdminStaff]


class ServiceListView(QuerysetFilteredMixin, generics.ListAPIView):
    """
    API endpoint that allows services to be viewed as list.
    """

    queryset = Service.objects.get_queryset().filter(active=True)
    serializer_class = ServiceListSelectSerializer
    filterset_class = ServiceListFilter
    permission_classes = [IsStaff]
