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
router.register("charge/items", ChargeItemViewSet, basename="charge-items")
router.register("charge/services", ChargeServiceViewSet, basename="charge-services")


app_name = "visits"

urlpatterns = [
    path(
        "slot/time/available/<date:date>/",
        VisitAvailableSlotsView.as_view(),
        name="slots-time-available",
    ),
    path(
        "slot/date/available/<uuid:patient>",
        VisitAvailableDatesView.as_view(),
        name="slots-date-available",
    ),
    path("visit/select/", SelectVisitView.as_view(), name="visit-select"),
    path("", include(router.urls)),
]
