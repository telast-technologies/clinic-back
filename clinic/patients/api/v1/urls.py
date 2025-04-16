from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.patients.api.v1.views import (
    PatientPrescriptionViewSet,
    PatientReportViewSet,
    PatientViewSet,
    SelectPatientView,
)

router = DefaultRouter()


router.register("patient", PatientViewSet, basename="patient")
router.register("patient_report", PatientReportViewSet, basename="patient_report")
router.register("patient_prescription", PatientPrescriptionViewSet, basename="patient_prescription")

app_name = "patients"

urlpatterns = [
    path("patient_select/", SelectPatientView.as_view(), name="patient_select"),
    path("", include(router.urls)),
]
