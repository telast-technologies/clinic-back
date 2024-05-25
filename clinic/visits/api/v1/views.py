from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from clinic.system_management.services.clinic_service import ClinicService
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff, IsStaff
from clinic.visits.api.v1.serializers import (
    AvailableDateListSerializer,
    AvailableSlotListSerializer,
    ChargeItemDetailSerializer,
    ChargeServiceDetailSerializer,
    ChargeServiceModifySerializer,
    CreateChargeItemSerializer,
    CreateVisitSerializer,
    SelectVisitSerializer,
    TimeSlotSerializer,
    UpdateChargeItemSerializer,
    UpdateVisitSerializer,
    VisitDetailSerializer,
)
from clinic.visits.filters import ChargeItemFilter, ChargeServiceFilter, SelectVisitFilter, TimeSlotFilter, VisitFilter
from clinic.visits.models import ChargeItem, ChargeService, TimeSlot, Visit


class TimeSlotViewSet(QuerysetFilteredMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows TimeSlot to be viewed or edited.
    """

    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    filterset_class = TimeSlotFilter
    permission_classes = [IsAdminStaff]


class VisitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visit to be viewed or edited.
    """

    queryset = Visit.objects.all()
    serializer_class = CreateVisitSerializer
    filterset_class = VisitFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset.filter(patient__clinic=self.request.user.staff.clinic)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return VisitDetailSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateVisitSerializer

        return super().get_serializer_class()


class SelectVisitView(generics.ListAPIView):
    queryset = Visit.objects.get_queryset().filter(date__gte=timezone.now().date())
    serializer_class = SelectVisitSerializer
    filterset_class = SelectVisitFilter
    permission_classes = [IsStaff]


@extend_schema_view(
    update=extend_schema(
        parameters=[
            OpenApiParameter(name="visit", description="Visit ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
    partial_update=extend_schema(
        parameters=[
            OpenApiParameter(name="visit", description="Visit ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
)
class ChargeItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ChargeItem to be viewed Created or edited.
    """

    queryset = ChargeItem.objects.all()
    serializer_class = CreateChargeItemSerializer
    filterset_class = ChargeItemFilter
    permission_classes = [IsStaff]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(visit__patient__clinic=self.request.user.staff.clinic)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateChargeItemSerializer
        if self.request.method in SAFE_METHODS:
            return ChargeItemDetailSerializer

        return super().get_serializer_class(*args, **kwargs)


class ChargeServiceViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint that allows ChargeService to be created or viewed.
    """

    queryset = ChargeService.objects.all()
    serializer_class = ChargeServiceModifySerializer
    filterset_class = ChargeServiceFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset.filter(visit__patient__clinic=self.request.user.staff.clinic)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ChargeServiceDetailSerializer
        return super().get_serializer_class()


class VisitAvailableSlotsView(views.APIView):
    """View for getting available slots for a given date."""

    serializer_class = None
    permission_classes = [IsStaff]

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
    """View for getting available dates for a patient for next 30 days including today."""

    serializer_class = None
    permission_classes = [IsStaff]

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
