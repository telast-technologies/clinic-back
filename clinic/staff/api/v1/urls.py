from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.staff.api.v1.views import StaffViewSet

router = DefaultRouter()


router.register("staff", StaffViewSet, basename="staff")


app_name = "staff"

urlpatterns = [
    path("", include(router.urls)),
]
