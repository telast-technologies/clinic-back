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

router.register("slots", TimeSlotViewSet, basename="slots")
router.register("visits", VisitViewSet, basename="visits")
router.register("charge/items", ChargeItemViewSet, basename="charge-items")
router.register("charge/services", ChargeServiceViewSet, basename="charge-services")


app_name = "visits"

urlpatterns = [
    path(
        "slots/time/available/<date:date>/",
        VisitAvailableSlotsView.as_view(),
        name="slots-time-available",
    ),
    path(
        "slots/date/available/<uuid:patient>",
        VisitAvailableDatesView.as_view(),
        name="slots-date-available",
    ),
    path("visits/select/", SelectVisitView.as_view(), name="visits-select"),
    path("", include(router.urls)),
]
