from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from clinic.patients.api.v1.serializers import PatientReportSerializer, PatientSerializer, SelectPatientSerializer
from clinic.patients.filters import PatientFilter, PatientReportFilter
from clinic.patients.models import Patient, PatientReport
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsStaff


class PatientViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PatientFilter
    search_fields = ["first_name", "last_name", "email", "phone", "nid", "uid"]
    ordering_fields = ["created_at"]


class SelectPatientView(QuerysetFilteredMixin, generics.ListAPIView):
    serializer_class = SelectPatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["first_name", "last_name", "email", "phone", "nid", "uid"]


class PatientReportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PatientReportSerializer
    queryset = PatientReport.objects.all()
    permission_classes = [IsStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PatientReportFilter

    def get_queryset(self):
        return super().get_queryset().filter(patient__clinic=self.request.user.staff.clinic)
