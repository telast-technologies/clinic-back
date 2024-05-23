from rest_framework import generics
from rest_framework.permissions import AllowAny

from clinic.system_management.api.v1.serializers import SelectExposedPermissionSerializer, SelectPackageSerializer
from clinic.system_management.filters import SelectPermissionFilter, SelectSelectFilter
from clinic.system_management.models import ExposedPermission, Package
from clinic.users.api.permissions import IsAdminStaff


class SelectPackageView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Package.objects.get_queryset().filter(active=True)
    serializer_class = SelectPackageSerializer
    filterset_class = SelectSelectFilter


class SelectPermissionView(generics.ListAPIView):
    permission_classes = [IsAdminStaff]
    queryset = ExposedPermission.objects.all()
    serializer_class = SelectExposedPermissionSerializer
    filterset_class = SelectPermissionFilter
