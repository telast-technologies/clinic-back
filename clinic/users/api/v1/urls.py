from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.users.api.v1.views import PatientViewSet, StaffViewSet

router = DefaultRouter()


router.register("staff", StaffViewSet, basename="staff")
router.register("patient", PatientViewSet, basename="patient")


app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
]
