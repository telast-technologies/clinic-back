from django.utils import timezone
from rest_framework import generics, mixins, viewsets

from clinic.invoices.api.v1.serializers import InvoiceSerializer, SelectVisitSerializer
from clinic.invoices.filters import InvoiceFilter
from clinic.invoices.models import Invoice
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
