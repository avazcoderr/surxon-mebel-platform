from rest_framework.pagination import PageNumberPagination
from utils.response_format import APIResponse


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that returns unified response format
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        Return a paginated response using the unified response format
        """
        return APIResponse.paginated_success(
            data=data,
            count=self.page.paginator.count,
            next_url=self.get_next_link(),
            previous_url=self.get_previous_link(),
            message="Products retrieved successfully"
        )