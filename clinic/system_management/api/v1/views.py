from rest_framework import generics
from rest_framework.permissions import AllowAny

from clinic.system_management.api.v1.serializers import ExposedPermissionSerializer, PackageSerializer
from clinic.system_management.filters import PermissionFilter
from clinic.system_management.models import ExposedPermission, Package
from clinic.users.api.permissions import IsAdminStaff


class PackageView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Package.objects.get_queryset().filter(active=True)
    serializer_class = PackageSerializer


class PermissionView(generics.ListAPIView):
    permission_classes = [IsAdminStaff]
    queryset = ExposedPermission.objects.all()
    serializer_class = ExposedPermissionSerializer
    filterset_class = PermissionFilter
