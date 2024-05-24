from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from clinic.system_management.services.clinic_service import ClinicService
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff, IsStaff
from clinic.utils.functions import convert_hours_to_times
from clinic.visits.api.v1.serializers import (
    AvailableSlotsSerializer,
    ChargeServiceDetailSerializer,
    ChargeServiceModifySerializer,
    CreateChargeItemSerializer,
    CreateVisitSerializer,
    ListChargeItemSerializer,
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
    queryset = Visit.objects.all()
    serializer_class = SelectVisitSerializer
    filterset_class = SelectVisitFilter
    permission_classes = [IsStaff]


class ChargeItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ChargeItem to be viewed Created or edited.
    """

    queryset = ChargeItem.objects.all()
    serializer_class = CreateChargeItemSerializer
    filterset_class = ChargeItemFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset.filter(visit__patient__clinic=self.request.user.staff.clinic)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateChargeItemSerializer
        if self.request.method in SAFE_METHODS:
            return ListChargeItemSerializer
        return super().get_serializer_class()


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
    serializer_class = None
    permission_classes = [IsStaff]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=AvailableSlotsSerializer,
                description="List of available slots for the given date",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={"hours": ["09:00:00", "11:00:00", "23:00:00", "00:00:00"]},
                    ),
                ],
            )
        }
    )
    def get(self, request, date, *args, **kwargs):
        clinic_handler = ClinicService(self.request.user.staff.clinic)
        available_time = clinic_handler.get_available_slots(date)
        return Response({"hours": convert_hours_to_times(available_time)}, status=status.HTTP_200_OK)