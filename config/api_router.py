from django.urls import include, path

v1 = [
    path("staff/", include("clinic.staff.api.v1.urls", namespace="staff")),
    path("patients/", include("clinic.patients.api.v1.urls", namespace="patients")),
    path("approvals/", include("clinic.approvals.api.urls", namespace="approvals")),
    path("system_management/", include("clinic.system_management.api.v1.urls", namespace="system_management")),
    path("healthcare/", include("clinic.healthcare.api.v1.urls", namespace="healthcare")),
    path("inventory/", include("clinic.inventory.api.v1.urls", namespace="inventory")),
    path("visits/", include("clinic.visits.api.v1.urls", namespace="visits")),
    path("invoices/", include("clinic.invoices.api.v1.urls", namespace="invoices")),
    path("users/", include("clinic.users.api.v1.urls", namespace="users")),
    path("dashboard/", include("clinic.dashboard.api.v1.urls", namespace="dashboard")),
]

urlpatterns = [
    path("v1/", include((v1, "v1"), namespace="v1")),
]
