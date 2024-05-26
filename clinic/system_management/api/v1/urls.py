from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.system_management.api.v1.views import ClinicProfileView, SelectPackageView, SelectPermissionView

router = DefaultRouter()


router.register("clinic", ClinicProfileView, basename="clinic")


app_name = "system_management"

urlpatterns = [
    path("package/select/", SelectPackageView.as_view(), name="package_select"),
    path("permissions/select/", SelectPermissionView.as_view(), name="permission_select"),
    path("", include(router.urls)),
]
