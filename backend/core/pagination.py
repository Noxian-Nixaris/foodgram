from rest_framework.pagination import PageNumberPagination
from core.constants import PAGE_SIZE


class PageCastomPaginator(PageNumberPagination):

    def get_page_size(self, request):
        if 'limit' in request.query_params:
            return request.query_params['limit']
        return PAGE_SIZE
