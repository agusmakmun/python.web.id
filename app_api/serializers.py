# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from rest_framework import serializers

from app_blog.models import (Tag, Post)
from app_user.models import Profile


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    total_posts = serializers.IntegerField(source='get_posts.count', read_only=True)

    class Meta:
        model = Tag
        fields = ('title', 'slug', 'total_posts')


class TagListSerializer(serializers.Field):

    def to_internal_value(self, data):
        # 'Django, Javscript Framework' => ['Django', 'Javscript Framework']
        return [title.strip() for title in data.split(',')]

    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag.title for tag in obj.all()]
        return obj


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    tags = TagListSerializer()
    total_visitors = serializers.IntegerField(source='get_visitors.count', read_only=True)
    total_favorites = serializers.IntegerField(source='get_favorites.count', read_only=True)

    class Meta:
        model = Post
        fields = ('author', 'title', 'slug', 'description',
                  'created', 'modified', 'publish', 'is_featured',
                  'tags', 'keywords', 'meta_description',
                  'rating_likes', 'rating_dislikes',
                  'total_visitors', 'total_favorites')
        read_only_fields = ('slug', 'is_featured', 'created',
                            'modified', 'rating_likes', 'rating_dislikes')

    def create(self, validated_data):
        tags_list = validated_data.pop('tags')
        instance = super(PostSerializer, self).create(validated_data)
        for title in tags_list:
            queryset = Tag.objects.filter(title__iexact=title)
            if queryset.exists():
                tag = queryset.first()
                instance.tags.add(tag)
        return instance

    def update(self, instance, validated_data):
        tags_list = validated_data.pop('tags')
        instance = super(PostSerializer, self).update(instance, validated_data)
        for title in tags_list:
            queryset = Tag.objects.filter(title__iexact=title)
            if queryset.exists():
                tag = queryset.first()
                instance.tags.add(tag)
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    last_login = serializers.CharField(source='user.last_login', read_only=True)
    date_joined = serializers.CharField(source='user.date_joined', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'last_login', 'date_joined',
                  'total_posts', 'total_favorites', 'total_featured_posts',
                  'display_name', 'location', 'about_me', 'website',
                  'twitter', 'linkedin', 'github', 'birth_date')
