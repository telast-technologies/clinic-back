from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class NotificationInboxPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"

    def paginate_queryset(self, queryset, request, view=None):
        queryset = super().paginate_queryset(queryset, request, view)
        for instance in queryset:
            instance.mark_as_read()
        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        return Response(
            {
                "max_pages": self.page.paginator.num_pages,
                **response.data,
            }
        )