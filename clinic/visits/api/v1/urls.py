from django.urls import include, path, register_converter
from rest_framework.routers import DefaultRouter

from clinic.visits.api.url_converters import DateConverter
from clinic.visits.api.v1.views import (
    ChargeItemViewSet,
    ChargeServiceViewSet,
    SelectVisitView,
    TimeSlotViewSet,
    VisitAvailableDatesView,
    VisitAvailableSlotsView,
    VisitViewSet,
)

router = DefaultRouter()

register_converter(DateConverter, "date")

router.register("slot", TimeSlotViewSet, basename="slot")
router.register("visit", VisitViewSet, basename="visit")
router.register("charge_items", ChargeItemViewSet, basename="charge_items")
router.register("charge_services", ChargeServiceViewSet, basename="charge_services")


app_name = "visits"

urlpatterns = [
    path(
        "slot/time/available/<date:date>/",
        VisitAvailableSlotsView.as_view(),
        name="slots_time_available",
    ),
    path(
        "slot/date/available/<uuid:patient>",
        VisitAvailableDatesView.as_view(),
        name="slots_date_available",
    ),
    path("visit_select/", SelectVisitView.as_view(), name="visit_select"),
    path("", include(router.urls)),
]
