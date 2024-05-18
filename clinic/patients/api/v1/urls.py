from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.patients.api.v1.views import PatientViewSet

router = DefaultRouter()


router.register("patient", PatientViewSet, basename="patient")


app_name = "patients"

urlpatterns = [
    path("", include(router.urls)),
]
