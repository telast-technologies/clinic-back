from django.urls import path

from clinic.system_management.api.v1.views import PackageView

app_name = "system_management"

urlpatterns = [
    path("packages/", PackageView.as_view(), name="packages"),
    path("permissions/", PackageView.as_view(), name="permissions"),
]
