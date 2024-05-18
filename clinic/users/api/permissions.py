from rest_framework.permissions import IsAuthenticated


class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, "staff")


class IsAdminStaff(IsStaff):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.staff.is_client_admin
