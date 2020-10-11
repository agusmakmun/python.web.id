# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from apps.blog.models.post import Post
from apps.blog.utils.slug import generate_unique_slug
from apps.api.base.views.base import BaseListCreateAPIView
from apps.api.versioned.v1.serializers.post import PostSerializer


class PostView(BaseListCreateAPIView):
    queryset = Post.objects.published()
    serializer_class = PostSerializer
    filterset_fields = ('author__username', 'tags__name', 'is_featured')
    search_fields = ('title', 'description', 'meta_description', 'keywords')
    model = Post

    def get_queryset(self):
        return super().get_queryset()\
                      .select_related('author')\
                      .prefetch_related('tags')

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, object_id):
        return super().retrieve(request, object_id)

    def post(self, request, *args, **kwargs):
        """
        function view to create the post object.
        :param `request` is request object.
        :return Response object.
        """
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)

        title = request.data.get('title')
        slug = generate_unique_slug(self.model, title)
        serializer.save(author=request.user, slug=slug, is_featured=False)

        headers = self.get_success_headers(serializer.data)
        response = {'status': status.HTTP_200_OK, 'result': serializer.data}
        return Response(response, status=response.get('status'), headers=headers)

    def put(self, request, *args, **kwargs):
        """
        function view to update the post object.
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

        if (instance.author != request.user):
            response = {'status': status.HTTP_400_BAD_REQUEST,
                        'message': _('Your are not allowed to update this post!')}
            return Response(response, status=response.get('status'))

        partial = kwargs.get('partial', True)
        serializer = self.get_serializer(instance, data=request.data, partial=partial,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(is_featured=instance.is_featured)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {'status': status.HTTP_200_OK, 'result': serializer.data}
        return Response(response, status=response.get('status'))

    def delete(self, request, *args, **kwargs):
        """
        function view to SOFT delete the post object.
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

        instance = get_object_or_404(self.model, id=object_id)

        if (instance.author != request.user):
            response = {'status': status.HTTP_400_BAD_REQUEST,
                        'message': _('Your are not allowed to delete this post!')}
            return Response(response, status=response.get('status'))

        # soft delete
        instance.deleted_at = timezone.now()
        instance.save()

        message = _('%(verbose_name)s successfully deleted!') % {'verbose_name': instance._meta.verbose_name}
        response = {'status': status.HTTP_200_OK, 'message': message}
        return Response(response, status=response.get('status'))
