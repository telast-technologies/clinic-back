class QuerysetFilteredMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, "staff"):
            return queryset.filter(clinic=user.staff.clinic)

        return queryset.none()
