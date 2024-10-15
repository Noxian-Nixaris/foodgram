from rest_framework.pagination import PageNumberPagination
from core.constants import PAGE_SIZE


class PageCastomPaginator(PageNumberPagination):
    page_size_query_param = 'limit'

