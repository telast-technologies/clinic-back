from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import SAFE_METHODS

from clinic.invoices.api.v1.serializers import (
    ChargeItemDetailSerializer,
    ChargeServiceDetailSerializer,
    ChargeServiceModifySerializer,
    CreateChargeItemSerializer,
    InvoiceSerializer,
    SelectVisitSerializer,
    UpdateChargeItemSerializer,
)
from clinic.invoices.filters import ChargeItemFilter, ChargeServiceFilter, InvoiceFilter
from clinic.invoices.models import ChargeItem, ChargeService, Invoice
from clinic.users.api.permissions import IsStaff


class InvoiceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows Invoice to be viewed or edited.
    """

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset.filter(visit__patient__clinic=self.request.user.staff.clinic)


class SelectInvoiceView(generics.ListAPIView):
    queryset = Invoice.objects.get_queryset().filter(created_at__date__gte=timezone.now().date())
    serializer_class = SelectVisitSerializer
    filterset_class = InvoiceFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset.filter(visit__patient__clinic=self.request.user.staff.clinic)


@extend_schema_view(
    update=extend_schema(
        parameters=[
            OpenApiParameter(name="invoice", description="Invoice ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
    partial_update=extend_schema(
        parameters=[
            OpenApiParameter(name="invoice", description="Invoice ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
    destroy=extend_schema(
        parameters=[
            OpenApiParameter(name="invoice", description="Invoice ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
)
class ChargeItemViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows ChargeItem to be viewed Created or edited.
    """

    queryset = ChargeItem.objects.all()
    serializer_class = CreateChargeItemSerializer
    filterset_class = ChargeItemFilter
    permission_classes = [IsStaff]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(invoice__visit__patient__clinic=self.request.user.staff.clinic)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateChargeItemSerializer
        if self.request.method in SAFE_METHODS:
            return ChargeItemDetailSerializer

        return super().get_serializer_class(*args, **kwargs)


@extend_schema_view(
    destroy=extend_schema(
        parameters=[
            OpenApiParameter(name="invoice", description="Invoice ID", required=True, type=OpenApiTypes.UUID),
        ]
    ),
)
class ChargeServiceViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint that allows ChargeService to be created or viewed.
    """

    queryset = ChargeService.objects.all()
    serializer_class = ChargeServiceModifySerializer
    filterset_class = ChargeServiceFilter
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset.filter(invoice__visit__patient__clinic=self.request.user.staff.clinic)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ChargeServiceDetailSerializer
        return super().get_serializer_class()
