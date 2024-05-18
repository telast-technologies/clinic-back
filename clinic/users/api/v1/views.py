from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsStaff
from clinic.users.api.v1.serializers import PatientSerializer, StaffDetailSerializer, StaffModifySerializer
from clinic.users.filters import PatientFilter, StaffFilter
from clinic.users.models import Patient, Staff


class StaffViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    serializer_class = StaffModifySerializer
    queryset = Staff.objects.all()
    filterset_class = StaffFilter
    permission_classes = [IsAuthenticated, IsStaff]

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.staff.pk)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return StaffDetailSerializer

        return super().get_serializer_class()


class PatientViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filterset_class = PatientFilter
    permission_classes = [IsAuthenticated, IsStaff]
