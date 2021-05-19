# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from apps.blog.models.post import Post
from apps.api.base.serializers.fields import DynamicFieldsModelSerializer
from apps.api.versioned.v1.serializers.tag import TagSerializer


class PostSerializer(DynamicFieldsModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, instance):
        return instance.get_absolute_url()

    def get_tags(self, instance):
        queryset = instance.tags.published()
        serializer = TagSerializer(queryset, many=True)
        return serializer.data

    def to_representation(self, instance):
        response_data = super().to_representation(instance).copy()
        response_data['tags'] = self.get_tags(instance)
        response_data['author'] = instance.author.username
        return response_data

    class Meta:
        model = Post
        exclude = ('publish', 'deleted_at')
        read_only_fields = ('slug', 'author')


class PostDetailSerializer(PostSerializer):
    total_visitors = serializers.SerializerMethodField()
    total_favorites = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()

    def get_total_visitors(self, instance):
        return instance.total_visitors

    def get_total_favorites(self, instance):
        return instance.total_favorites

    def get_total_likes(self, instance):
        return instance.rating.likes

    def get_total_dislikes(self, instance):
        return instance.rating.dislikes
