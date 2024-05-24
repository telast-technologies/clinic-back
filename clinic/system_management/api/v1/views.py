from typing import Any

from rest_framework import generics
from rest_framework.permissions import AllowAny

from clinic.system_management.api.v1.serializers import (
    ClinicSerializer,
    SelectExposedSelectPermissionSerializer,
    SelectPackageSerializer,
)
from clinic.system_management.filters import SelectPackageFilter, SelectPermissionFilter
from clinic.system_management.models import ExposedPermission, Package
from clinic.users.abstracts.views import ProfileUpdateViewSet
from clinic.users.api.permissions import IsAdminStaff


class ClinicProfileView(ProfileUpdateViewSet):
    serializer_class = ClinicSerializer
    permission_classes = [IsAdminStaff]

    def get_object(self) -> Any:
        return self.request.user.staff.clinic


class SelectPackageView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Package.objects.get_queryset().filter(active=True)
    serializer_class = SelectPackageSerializer
    filterset_class = SelectPackageFilter


class SelectPermissionView(generics.ListAPIView):
    permission_classes = [IsAdminStaff]
    queryset = ExposedPermission.objects.all()
    serializer_class = SelectExposedSelectPermissionSerializer
    filterset_class = SelectPermissionFilter
