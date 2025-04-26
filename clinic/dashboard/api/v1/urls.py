from django.urls import path, register_converter

from clinic.dashboard.api.v1.views import ExportPatientsView, VisitDashboardView
from clinic.visits.api.url_converters import DateConverter

register_converter(DateConverter, "date")


app_name = "dashboard"

urlpatterns = [
    path("visit/<date:start_date>/<date:end_date>/", VisitDashboardView.as_view(), name="visit"),
    path("export_patients", ExportPatientsView.as_view(), name="export_patients"),
]
