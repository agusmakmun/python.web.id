# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils import timezone
from django.db.models import (Q, Count)

from apps.blog.models.tag import Tag
from apps.blog.models.post import Post
from apps.blog.models.addons import Visitor

register = template.Library()


@register.simple_tag
def popular_tags(limit=5, query=None):
    """
    {% load post_tags %}
    {% popular_tags as popular_tags_list %}
    {% for tag in popular_tags_list %}
      <a href="{% url 'apps.blog:post_list_tagged' slug=tag.slug %}">
        {{ tag.slug }} <span class="badge">{{ tag.total }}</span>
      </a>
    {% endfor %}

    used in:
        - templates/apps/blog/post/list.html
    """
    if query:
        queryset = Tag.objects.published()\
                              .filter(Q(name__startswith=query))
    else:
        queryset = Tag.objects.published()

    maps = [
        {'tag': tag, 'total': tag.post_set.published().count()}
        for tag in queryset
    ]
    maps.sort(key=lambda x: x['total'], reverse=True)
    return maps[:limit]


# @register.simple_tag
# def hot_posts(limit=5):
#     """
#     {% load post_tags %}
#     {% hot_posts as hot_posts_list %}
#     {% for post in hot_posts_list %}
#       <a href="{% url 'posts_detail' slug=post.slug %}">{{ post.title }}</a>
#     {% endfor %}
#     used in:
#         - apps/blog/posts_list.html
#     """
#     queryset = Post.objects.published().order_by('-rating_likes')
#     top_posts = Visitor.objects.filter(post__in=queryset).values('post')\
#         .annotate(total=Count('post__pk')).order_by('-total')
#     id_top_posts = [pk['post'] for pk in top_posts]
#     filter_posts = list(queryset.filter(pk__in=id_top_posts,
#                                         modified__month=timezone.now().month,
#                                         modified__year=timezone.now().year))
#     queryset = sorted(filter_posts, key=lambda i: id_top_posts.index(i.pk))
#     return queryset[:limit]


@register.simple_tag
def random_posts(limit=5):
    """
    {% load post_tags %}
    {% random_posts as random_posts_list %}
    {% for post in random_posts_list %}
      <a href="{% url 'posts_detail' slug=post.slug %}">{{ post.title }}</a>
    {% endfor %}
    used in:
        - templates/apps/blog/post/includes/sidebar_list.html
    """
    return Post.objects.published().order_by('-rating_likes').order_by('?')[:limit]
