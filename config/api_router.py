from django.urls import include, path

v1 = [
    path("users/", include("clinic.users.api.v1.urls", namespace="users")),
    path("system_management/", include("clinic.system_management.api.v1.urls", namespace="system_management")),
]

urlpatterns = [
    path("v1/", include((v1, "v1"), namespace="v1")),
]
