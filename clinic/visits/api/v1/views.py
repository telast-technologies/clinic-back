from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status, views, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from clinic.system_management.services.clinic_service import ClinicService
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff
from clinic.visits.api.v1.serializers import (
    AvailableDateListSerializer,
    AvailableSlotListSerializer,
    CreateVisitSerializer,
    TimeSlotSerializer,
    UpdateVisitSerializer,
    VisitDetailSerializer,
)
from clinic.visits.filters import TimeSlotFilter, VisitFilter
from clinic.visits.mixins.v1.views import VisitFlowViewMixin, VisitViewMixin
from clinic.visits.models import TimeSlot, Visit


class TimeSlotViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows TimeSlot to be viewed or edited.
    """

    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = TimeSlotFilter
    search_fields = ["uid"]
    ordering_fields = ["created_at"]
    filter_field = "clinic"


class VisitViewSet(QuerysetFilteredMixin, VisitViewMixin, VisitFlowViewMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Visit to be viewed or edited.
    """

    queryset = Visit.objects.all()
    serializer_class = CreateVisitSerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = VisitFilter
    search_fields = ["uid", "no", "patient__medical_number", "patient__first_name", "patient__last_name"]
    ordering_fields = ["created_at"]
    filter_field = "patient__clinic"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return VisitDetailSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateVisitSerializer

        return super().get_serializer_class()


class VisitAvailableSlotsView(views.APIView):
    """View for getting available slots for a given date."""

    serializer_class = None
    permission_classes = [IsAdminStaff]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=AvailableSlotListSerializer,
                description="List of available slots for the given date",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={"slots": ["09:00:00", "11:00:00", "23:00:00", "00:00:00"]},
                    ),
                ],
            )
        }
    )
    def get(self, request, date, *args, **kwargs):
        # initial clinic service
        clinic_handler = ClinicService(request.user.staff.clinic)
        # get all available slot
        available_slots = clinic_handler.get_available_slots(date)
        # return response
        return Response(
            AvailableSlotListSerializer({"slots": available_slots}, read_only=True).data, status=status.HTTP_200_OK
        )


class VisitAvailableDatesView(views.APIView):
    """View for getting available dates for a patient for next 31 days including today."""

    serializer_class = None
    permission_classes = [IsAdminStaff]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=AvailableDateListSerializer,
                description="List of available dates for the patient",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={"dates": ["2022-01-01", "2022-01-02", "2022-01-03"]},
                    ),
                ],
            )
        }
    )
    def get(self, request, patient, *args, **kwargs):
        # initial clinic service
        clinic_handler = ClinicService(request.user.staff.clinic)
        # get all available dates
        available_dates = clinic_handler.get_available_dates(patient)
        # return response
        return Response(
            AvailableDateListSerializer({"dates": available_dates}, read_only=True).data, status=status.HTTP_200_OK
        )
