from typing import Any

from rest_framework.permissions import IsAuthenticated

from clinic.system_management.api.v1.serializers import ClinicSerializer
from clinic.users.abstracts.views import ProfileViewSet
from clinic.users.api.permissions import IsStaff


class ClinicViewSet(ProfileViewSet):
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def get_object(self) -> Any:
        return self.request.user.staff.clinic
