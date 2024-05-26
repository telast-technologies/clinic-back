from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.inventory.api.v1.views import SelectSupplyViewSet, SupplyViewSet

router = DefaultRouter()


router.register("supply", SupplyViewSet, basename="supply")


app_name = "inventory"

urlpatterns = [
    path("supply/select/", SelectSupplyViewSet.as_view(), name="supply-select"),
    path("", include(router.urls)),
]
