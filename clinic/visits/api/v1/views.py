from rest_framework import viewsets

from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff
from clinic.visits.api.v1.serializers import TimeSlotSerializer
from clinic.visits.filters import TimeSlotFilter
from clinic.visits.models import TimeSlot


class TimeSlotViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows TimeSlot to be viewed or edited.
    """

    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    filterset_class = TimeSlotFilter
    permission_classes = [IsAdminStaff]
