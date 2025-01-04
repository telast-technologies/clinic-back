from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS

from clinic.invoices.api.v1.serializers import (
    ChargeItemDetailSerializer,
    ChargeServiceDetailSerializer,
    ChargeServiceModifySerializer,
    CreateChargeItemSerializer,
    InvoiceSerializer,
    SelectInvoiceSerializer,
    UpdateChargeItemSerializer,
)
from clinic.invoices.filters import ChargeItemFilter, ChargeServiceFilter, InvoiceFilter
from clinic.invoices.models import ChargeItem, ChargeService, Invoice
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff


class InvoiceViewSet(
    QuerysetFilteredMixin,
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
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = InvoiceFilter
    search_fields = [
        "uid",
        "no",
        "visit__no",
        "visit__patient__medical_number",
        "visit__patient__first_name",
        "visit__patient__last_name",
    ]
    ordering_fields = ["created_at", "tax", "discount", "sub_total"]
    filter_field = "visit__patient__clinic"


class SelectInvoiceView(QuerysetFilteredMixin, generics.ListAPIView):
    queryset = Invoice.objects.get_queryset()
    serializer_class = SelectInvoiceSerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = InvoiceFilter
    search_fields = [
        "uid",
        "no",
        "visit__no",
        "visit__patient__medical_number",
        "visit__patient__first_name",
        "visit__patient__last_name",
    ]
    ordering_fields = ["created_at", "tax", "discount", "sub_total"]
    filter_field = "visit__patient__clinic"


class ChargeItemViewSet(
    QuerysetFilteredMixin,
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
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ChargeItemFilter
    search_fields = ["uid"]
    ordering_fields = ["created_at"]
    filter_field = "invoice__visit__patient__clinic"

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateChargeItemSerializer
        if self.request.method in SAFE_METHODS:
            return ChargeItemDetailSerializer

        return super().get_serializer_class(*args, **kwargs)


class ChargeServiceViewSet(
    QuerysetFilteredMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows ChargeService to be created or viewed.
    """

    queryset = ChargeService.objects.all()
    serializer_class = ChargeServiceModifySerializer
    permission_classes = [IsAdminStaff]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ChargeServiceFilter
    search_fields = ["uid"]
    ordering_fields = ["created_at"]
    filter_field = "invoice__visit__patient__clinic"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ChargeServiceDetailSerializer
        return super().get_serializer_class()
