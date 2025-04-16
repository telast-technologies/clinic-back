from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clinic.users.api.v1.views import NotificationInboxViewSet

app_name = "users"

router = DefaultRouter()

router.register("notification_inbox", NotificationInboxViewSet, basename="notification_inbox")

urlpatterns = [
    path("", include(router.urls)),
]