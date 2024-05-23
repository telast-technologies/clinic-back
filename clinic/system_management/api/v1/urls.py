from django.urls import path

from clinic.system_management.api.v1.views import SelectPackageView, SelectPermissionView

app_name = "system_management"

urlpatterns = [
    path("packages/", SelectPackageView.as_view(), name="packages"),
    path("permissions/", SelectPermissionView.as_view(), name="permissions"),
]
