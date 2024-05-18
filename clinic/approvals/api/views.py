from rest_framework import mixins, viewsets

from clinic.approvals.api.serializers import JoinRequestSerializer
from clinic.approvals.models import JoinRequest


class JoinRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = JoinRequestSerializer
    queryset = JoinRequest.objects.all()
    permission_classes = []
