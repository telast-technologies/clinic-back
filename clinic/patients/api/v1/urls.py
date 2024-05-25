from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.patients.api.v1.views import PatientReportViewSet, PatientViewSet, SelectPatientView

router = DefaultRouter()


router.register("patient", PatientViewSet, basename="patient")
router.register("patient/report", PatientReportViewSet, basename="patient-report")

app_name = "patients"

urlpatterns = [
    path("patient/select/", SelectPatientView.as_view(), name="patient-select"),
    path("", include(router.urls)),
]
