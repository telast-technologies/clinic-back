class QuerysetFilteredMixin:
    filter_field = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, "staff"):
            return queryset.filter(**{self.filter_field: user.staff.clinic})

        return queryset.none()
