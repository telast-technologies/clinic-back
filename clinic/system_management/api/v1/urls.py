from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.system_management.api.v1.views import ClinicViewSet

router = DefaultRouter()


router.register("clinic", ClinicViewSet, basename="clinic")


app_name = "system_management"

urlpatterns = [
    path("", include(router.urls)),
]
