from django.urls import include, path
from clinic.invoices.api.v1.views import InvoiceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("invoice", InvoiceViewSet, basename="invoice")

app_name = "invoices"

urlpatterns = [
    path("", include(router.urls)),
]
