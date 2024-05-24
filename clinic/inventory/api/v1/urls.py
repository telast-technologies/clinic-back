from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.inventory.api.v1.views import SelectSupplyViewSet, SupplyViewSet

router = DefaultRouter()


router.register("supplies", SupplyViewSet, basename="supplies")


app_name = "inventory"

urlpatterns = [
    path("supplies_select/", SelectSupplyViewSet.as_view(), name="supplies-select"),
    path("", include(router.urls)),
]
