from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.healthcare.api.v1.views import ServiceListView, ServiceViewset

router = DefaultRouter()


router.register("services", ServiceViewset, basename="services")


app_name = "healthcare"

urlpatterns = [
    path("services/select/", ServiceListView.as_view(), name="services-select"),
    path("", include(router.urls)),
]
