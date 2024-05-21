from django.urls import include, path

v1 = [
    path("staff/", include("clinic.staff.api.v1.urls", namespace="staff")),
    path("patients/", include("clinic.patients.api.v1.urls", namespace="patients")),
    path("approvals/", include("clinic.approvals.api.urls", namespace="approvals")),
    path("system_management/", include("clinic.system_management.api.v1.urls", namespace="system_management")),
    path("healthcare/", include("clinic.healthcare.api.v1.urls", namespace="healthcare")),
    path("inventory/", include("clinic.inventory.api.v1.urls", namespace="inventory")),
]

urlpatterns = [
    path("v1/", include((v1, "v1"), namespace="v1")),
]
