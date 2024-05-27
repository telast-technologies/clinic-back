from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
from rest_framework import generics, mixins, viewsets

from clinic.patients.api.v1.serializers import PatientReportSerializer, PatientSerializer, SelectPatientSerializer
from clinic.patients.filters import PatientFilter, PatientReportFilter, SelectPatientFilter
from clinic.patients.models import Patient, PatientReport
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsStaff


class PatientViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filterset_class = PatientFilter
    permission_classes = [IsStaff]


class SelectPatientView(QuerysetFilteredMixin, generics.ListAPIView):
    serializer_class = SelectPatientSerializer
    queryset = Patient.objects.all()
    filterset_class = SelectPatientFilter
    permission_classes = [IsStaff]


@extend_schema_view(
    destroy=extend_schema(
        parameters=[
            OpenApiParameter(name="patient", description="Patient ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
)
class PatientReportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PatientReportSerializer
    queryset = PatientReport.objects.all()
    filterset_class = PatientReportFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return super().get_queryset().filter(patient__clinic=self.request.user.staff.clinic)
