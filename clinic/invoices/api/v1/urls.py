from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.invoices.api.v1.views import InvoiceViewSet

router = DefaultRouter()

router.register("invoice", InvoiceViewSet, basename="invoice")

app_name = "invoices"

urlpatterns = [
    path("", include(router.urls)),
]
