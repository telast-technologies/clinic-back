from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.approvals.api.views import JoinRequestViewSet

router = DefaultRouter()


router.register("join_request", JoinRequestViewSet, basename="join_request")


app_name = "approvals"

urlpatterns = [
    path("", include(router.urls)),
]
