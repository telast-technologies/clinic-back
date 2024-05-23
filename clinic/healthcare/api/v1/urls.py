from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.healthcare.api.v1.views import SelectServiceView, ServiceViewSet

router = DefaultRouter()


router.register("services", ServiceViewSet, basename="services")


app_name = "healthcare"

urlpatterns = [
    path("services/select/", SelectServiceView.as_view(), name="services-select"),
    path("", include(router.urls)),
]
