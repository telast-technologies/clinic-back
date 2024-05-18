from rest_framework import viewsets

from clinic.patients.api.v1.serializers import PatientSerializer
from clinic.patients.filters import PatientFilter
from clinic.patients.models import Patient
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsStaff


class PatientViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filterset_class = PatientFilter
    permission_classes = [IsStaff]
