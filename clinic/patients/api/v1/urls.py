from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.patients.api.v1.views import PatientReportViewSet, PatientViewSet

router = DefaultRouter()


router.register("patient", PatientViewSet, basename="patient")
router.register("patient_report", PatientReportViewSet, basename="patient_report")

app_name = "patients"

urlpatterns = [
    path("", include(router.urls)),
]
