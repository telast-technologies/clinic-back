from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.inventory.api.v1.views import SupplyViewSet

router = DefaultRouter()


router.register("supplies", SupplyViewSet, basename="supplies")


app_name = "inventory"

urlpatterns = [
    path("", include(router.urls)),
]
