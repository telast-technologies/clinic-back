from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.visits.api.v1.views import TimeSlotViewSet

router = DefaultRouter()


router.register("time_slots", TimeSlotViewSet, basename="time_slots")


app_name = "visits"

urlpatterns = [
    path("", include(router.urls)),
]
