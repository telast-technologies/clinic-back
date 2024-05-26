from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.healthcare.api.v1.views import SelectServiceView, ServiceViewSet

router = DefaultRouter()


router.register("service", ServiceViewSet, basename="service")


app_name = "healthcare"

urlpatterns = [
    path("service/select/", SelectServiceView.as_view(), name="service-select"),
    path("", include(router.urls)),
]
