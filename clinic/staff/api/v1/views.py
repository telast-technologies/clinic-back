from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from clinic.staff.api.v1.serializers import StaffDetailSerializer, StaffListSerializer, StaffModifySerializer
from clinic.staff.filters import StaffFilter
from clinic.staff.models import Staff
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsStaff


class StaffViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    serializer_class = StaffModifySerializer
    queryset = Staff.objects.all()
    filterset_class = StaffFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.staff.pk)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS and self.action == "retrieve":
            return StaffDetailSerializer
        if self.request.method in SAFE_METHODS:
            return StaffListSerializer

        return super().get_serializer_class()
