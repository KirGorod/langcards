from rest_framework.pagination import LimitOffsetPagination


class SiteCommentsPagination(LimitOffsetPagination):
    default_limit = 10
