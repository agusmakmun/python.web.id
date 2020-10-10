# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apps.api.base.serializers.fields import DynamicFieldsModelSerializer
from apps.blog.models.tag import Tag


class TagSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'description')
