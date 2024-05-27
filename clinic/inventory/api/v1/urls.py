from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.inventory.api.v1.views import SelectSupplyViewSet, SupplyViewSet

router = DefaultRouter()


router.register("supply", SupplyViewSet, basename="supply")


app_name = "inventory"

urlpatterns = [
    path("supply_select/", SelectSupplyViewSet.as_view(), name="supply_select"),
    path("", include(router.urls)),
]
