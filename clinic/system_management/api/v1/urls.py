from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.system_management.api.v1.views import ClinicProfileView, SelectPackageView, SelectPermissionView

router = DefaultRouter()


router.register("clinic", ClinicProfileView, basename="clinic")


app_name = "system_management"

urlpatterns = [
    path("packages/", SelectPackageView.as_view(), name="packages"),
    path("permissions/", SelectPermissionView.as_view(), name="permissions"),
    path("", include(router.urls)),
]
