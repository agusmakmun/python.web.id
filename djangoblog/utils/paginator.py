# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.conf import settings
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class RestPagination(PageNumberPagination):
    """
    class FoobarPagiantion(RestPagination):
        page_size = 10


    class FoobarView(ListAPIView):
        pagination_class = FoobarPagiantion
    """

    def paginate_queryset(self, queryset, request, view=None):
        # self.count_objects = queryset.filter(id__gt=2).count()
        return super(RestPagination, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, results):
        next_link = self.get_next_link() if self.get_next_link() is not None else ''
        prev_link = self.get_previous_link() if self.get_previous_link() is not None else ''

        if settings.USE_SSL:
            next_link = next_link.replace('http:', 'https:')
            prev_link = prev_link.replace('http:', 'https:')

        return Response(OrderedDict([
            # ('count_objects', self.count_objects),
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('next', next_link if next_link != '' else None),
            ('previous', prev_link if prev_link != '' else None),
            ('status', status.HTTP_200_OK),
            ('results', results)
        ]))
