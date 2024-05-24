from django.urls import include, path, register_converter
from rest_framework.routers import DefaultRouter

from clinic.visits.api.url_converters import DateConverter
from clinic.visits.api.v1.views import (
    ChargeItemViewSet,
    ChargeServiceViewSet,
    SelectVisitView,
    TimeSlotViewSet,
    VisitAvailableSlotsView,
    VisitViewSet,
)

router = DefaultRouter()

register_converter(DateConverter, "date")

router.register("time_slots", TimeSlotViewSet, basename="time_slots")
router.register("visits", VisitViewSet, basename="visits")
router.register("charge_items", ChargeItemViewSet, basename="charge_items")
router.register("charge_services", ChargeServiceViewSet, basename="charge_services")


app_name = "visits"

urlpatterns = [
    path(
        "available_slots/<date:date>/",
        VisitAvailableSlotsView.as_view(),
        name="available_slots",
    ),
    path("visits_select/", SelectVisitView.as_view(), name="visits-select"),
    path("", include(router.urls)),
]
