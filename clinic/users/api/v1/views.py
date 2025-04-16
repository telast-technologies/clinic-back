from notifications.models import Notification
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from clinic.users.api.pagination import NotificationInboxPagination
from clinic.users.api.v1.serializers import NotificationInboxSerializer


class NotificationInboxViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    querySet = Notification.objects.all().order_by("-unread", "-timestamp")
    serializer_class = NotificationInboxSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationInboxPagination

    def get_queryset(self, *args, **kwargs):
        return self.request.user.notifications.all()