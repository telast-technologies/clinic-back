from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.system_management.api.v1.views import ClinicProfileView, SelectPackageView, SelectPermissionView

router = DefaultRouter()


router.register("clinic", ClinicProfileView, basename="clinic")


app_name = "system_management"

urlpatterns = [
    path("package_select/", SelectPackageView.as_view(), name="package_select"),
    path("permissions_select/", SelectPermissionView.as_view(), name="permissions_select"),
    path("", include(router.urls)),
]
