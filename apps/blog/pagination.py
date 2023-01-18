from rest_framework.pagination import PageNumberPagination

class SmallSetPagination(PageNumberPagination):
    page_query_param="p"
    page_size=6
    max_page_size=6
    page_size_query_param="page_size"

class MediumSetPagination(PageNumberPagination):
    page_query_param="p"
    page_size=9
    max_page_size=9
    page_size_query_param="page_size"

class LargeSetPagination(PageNumberPagination):
    page_query_param="p"
    page_size=18
    max_page_size=18
    page_size_query_param="page_size"