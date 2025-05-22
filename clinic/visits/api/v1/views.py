from collections import defaultdict

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status, views, viewsets
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
    VisitQueueSerializer,
    VisitReOrderQueueSerializer,
)
from clinic.visits.choices import VisitStatus
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


class TodayQueueAPIView(views.APIView):
    permission_classes = [IsAdminStaff]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=VisitQueueSerializer,
                description="List of available queues for the patient",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "examination": [
                                {"visit_no": 1, "patient": "John Doe", "queue": 1},
                                {"visit_no": 2, "patient": "Jane Doe", "queue": 2},
                            ],
                            "consultant": [{"visit_no": 3, "patient": "Alice Smith", "queue": 1}],
                        },
                    ),
                ],
            )
        }
    )
    def get(self, request):
        today = timezone.now().date()
        visits = Visit.objects.filter(
            patient__clinic=request.user.staff.clinic, arrival_info__date=f"{today}", status=VisitStatus.ARRIVED
        )

        categorized_queue = defaultdict(list)
        for visit in visits:
            purpose = visit.arrival_info.get("purpose")
            queue_value = visit.arrival_info.get("queue")
            if purpose is not None and queue_value is not None:
                categorized_queue[purpose].append(
                    {
                        "visit_no": visit.no,
                        "visit_pk": visit.pk,
                        "patient": visit.patient.get_full_name(),
                        "queue": queue_value,
                    }
                )

        # Sort each purpose list by 'queue' ascending
        for purpose in categorized_queue:
            categorized_queue[purpose] = sorted(categorized_queue[purpose], key=lambda x: x["queue"])

        return Response(categorized_queue)


class ReorderQueueAPIView(views.APIView):
    permission_classes = [IsAdminStaff]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=VisitQueueSerializer,
                description="List of available queues for the patient",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "examination": [
                                {"visit_pk": "1", "visit_no": "1", "patient": "John Doe", "queue": 1},
                                {"visit_pk": "2", "visit_no": "2", "patient": "Jane Doe", "queue": 2},
                            ],
                            "consultant": [{"visit_pk": "3", "visit_no": "3", "patient": "Alice Smith", "queue": 1}],
                            "bandage": [{"visit_pk": "4", "visit_no": "5", "patient": "Bob Smith", "queue": 1}],
                            "injection": [{"visit_pk": "6", "visit_no": "7", "patient": "Bob Smith", "queue": 1}],
                        },
                    ),
                ],
            )
        },
        request=inline_serializer(
            name="VisitReorderRequest",
            many=True,
            fields={
                "visit_pk": serializers.CharField(),
                "queue": serializers.IntegerField(),
            },
        ),
    )
    def patch(self, request):
        serializer = VisitReOrderQueueSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        today = timezone.now().date()
        visits = Visit.objects.filter(
            patient__clinic=request.user.staff.clinic,
            pk__in=[visit["visit_pk"] for visit in serializer.validated_data],
            arrival_info__date=f"{today}",
            status=VisitStatus.ARRIVED,
        )

        categorized_queue = defaultdict(list)
        for visit in visits:
            visit.arrival_info["queue"] = next(
                (v["queue"] for v in serializer.validated_data if v["visit_pk"] == visit.pk), None
            )
            visit.save()

            purpose = visit.arrival_info.get("purpose")
            queue_value = visit.arrival_info.get("queue")
            if purpose is not None and queue_value is not None:
                categorized_queue[purpose].append(
                    {
                        "visit_no": visit.no,
                        "visit_pk": visit.pk,
                        "patient": visit.patient.get_full_name(),
                        "queue": queue_value,
                    }
                )

        # Sort each purpose list by 'queue' ascending
        for purpose in categorized_queue:
            categorized_queue[purpose] = sorted(categorized_queue[purpose], key=lambda x: x["queue"])

        return Response(categorized_queue)
