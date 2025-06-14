from rest_framework import pagination
from rest_framework.response import Response


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        return Response(
            {
                "max_pages": self.page.paginator.num_pages,
                **response.data,
            }
        )
