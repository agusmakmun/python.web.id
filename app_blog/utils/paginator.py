# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from rest_framework.pagination import PageNumberPagination


class GenericPaginator(object):

    """
    class PostList(GenericPaginator, ListView):
        ....

        context_data['page_range'] = self.get_page_range()
    """

    def get_page_range(self):
        page = self.request.GET.get('page')
        paginate_by = self.paginate_by or 10
        queryset = self.queryset or self.get_queryset()

        # if page is None:
        #    raise Exception('request `?page` is None')

        paginator = Paginator(queryset, paginate_by)

        try:
            tutorials = paginator.page(page)
        except PageNotAnInteger:
            tutorials = paginator.page(1)
        except EmptyPage:
            tutorials = paginator.page(paginator.num_pages)

        index = tutorials.number - 1
        limit = 3  # limit for show range left and right of number pages
        max_index = len(paginator.page_range)
        start_index = index - limit if index >= limit else 0
        end_index = index + limit if index <= max_index - limit else max_index

        # When you return this, you will getting error
        # `page_range TypeError: sequence index must be integer, not 'slice'`.
        # Because now in django changelog, use `xrange`, and not `range`.
        # See this tickets: https://code.djangoproject.com/ticket/23140
        # >>> page_range  = paginator.page_range[start_index:end_index]
        page_range = list(paginator.page_range)[start_index:end_index]
        return page_range


class StandardRestAPIPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class LongRestAPIPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
