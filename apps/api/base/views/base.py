"""
Base API views
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, ListAPIView, ListCreateAPIView)


class BaseAPIMixin:
    """
    This `BaseAPIMixin` used to handle
    all default `rest_framework.generics` views.
    """
    model = None  # should be model class, e.g: 'apps.blog.models.post.Post'
    serializer_class = None  # should be serializer class.

    def get_serializer_context(self):
        """
        we provide the `request` as default serializer context.
        this case to handle the additional context into serializer.
        """
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        """
        just fetch from base class `ListAPIView` or `ListCreateAPIView`.
        :param `request` is request object.
        :return Response object.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, object_id):
        """
        custom retrieve function with validating the `object_id`,
        just makesure that `object_id` value provided as Integer/Digit value.
        :param `request` is request object.
        :param `object_id` is integer id of retrieved object.
        :return Response object.
        """
        if not str(object_id).isdigit():
            response = {'status': status.HTTP_400_BAD_REQUEST,
                        'message': _('Argument id should be integer!')}
            return Response(response, status=response.get('status'))

        instance = get_object_or_404(self.model, id=object_id, deleted_at__isnull=True)
        serializer = self.serializer_class(instance, many=False,
                                           context=self.get_serializer_context())
        response = {'status': status.HTTP_200_OK, 'result': serializer.data}
        return Response(response, status=response.get('status'))

    def get(self, request, *args, **kwargs):
        """
        See `self.retrieve(...)` and `self.list(...)` functions.
        """
        object_id = request.GET.get('id')
        if object_id is not None:
            return self.retrieve(request, object_id)
        return self.list(request, *args, *kwargs)


class BaseCreateAPIMixin(BaseAPIMixin):
    """ Base Create API Mixin """

    def post(self, request, *args, **kwargs):
        """
        custom base `post` function with adding the `request` object into serializer context.
        also excepting the invalidated serializer fields.
        :param `request` is request object.
        :return Response object.
        """
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {'status': status.HTTP_200_OK, 'result': serializer.data}
        return Response(response, status=response.get('status'), headers=headers)

    def put(self, request, *args, **kwargs):
        """
        custom base `put` function with validating the `object_id` value.
        just makesure that `object_id` is not None, and the value of `id` as Integer/Digit.
        :param `request` is request object.
        :return Response object.
        """
        if ('pk' not in request.data) and ('id' not in request.data):
            response = {'status': status.HTTP_400_BAD_REQUEST,
                        'message': _('KeyError argument id is required!')}
            return Response(response, status=response.get('status'))

        object_id = request.data['pk'] if 'pk' in request.data else request.data['id']
        if not str(object_id).isdigit():
            response = {'status': status.HTTP_400_BAD_REQUEST,
                        'message': _('Argument id should be integer!')}
            return Response(response, status=response.get('status'))

        instance = get_object_or_404(self.model, id=object_id, deleted_at__isnull=True)
        partial = kwargs.get('partial', True)

        serializer = self.get_serializer(instance, data=request.data, partial=partial,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {'status': status.HTTP_200_OK, 'result': serializer.data}
        return Response(response, status=response.get('status'))


class BaseListAPIView(BaseAPIMixin, ListAPIView):
    """ Base List API View """
    allowed_methods = ('get',)


class BaseCreateAPIView(BaseCreateAPIMixin, CreateAPIView):
    """ Base Create API View """
    pass


class BaseListCreateAPIView(BaseCreateAPIMixin, ListCreateAPIView):
    """ Base List Create API View """
    pass
