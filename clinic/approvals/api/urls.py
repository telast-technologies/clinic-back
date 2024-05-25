from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.approvals.api.views import JoinRequestViewSet

router = DefaultRouter()


router.register("request/join", JoinRequestViewSet, basename="request-join")


app_name = "approvals"

urlpatterns = [
    path("", include(router.urls)),
]
