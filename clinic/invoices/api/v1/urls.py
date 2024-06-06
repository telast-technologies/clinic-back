from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.invoices.api.v1.views import InvoiceViewSet, SelectInvoiceView

router = DefaultRouter()

router.register("invoice", InvoiceViewSet, basename="invoice")

app_name = "invoices"

urlpatterns = [
    path("invoice_select/", SelectInvoiceView.as_view(), name="invoice_select"),
    path("", include(router.urls)),
]
