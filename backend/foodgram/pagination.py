from rest_framework.pagination import PageNumberPagination


class CartCustomPagination(PageNumberPagination):
    """
    Custom pagination class
    Names of constants speak for themselves.
    """
    page_size = 6
    page_size_query_param = 'limit'
