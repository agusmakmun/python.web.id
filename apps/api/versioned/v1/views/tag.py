# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apps.blog.models.tag import Tag
from apps.api.base.views.base import BaseListAPIView
from apps.api.versioned.v1.serializers.tag import TagSerializer


class TagView(BaseListAPIView):
    queryset = Tag.objects.published()
    serializer_class = TagSerializer
    filterset_fields = ('name', )
    search_fields = ('name', 'description')
    model = Tag

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, object_id):
        return super().retrieve(request, object_id)
