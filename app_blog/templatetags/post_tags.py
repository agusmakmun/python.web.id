# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils import timezone
from django.db.models import (Q, Count)

from app_blog.models import (Post, Tag, Visitor)

register = template.Library()


@register.simple_tag
def popular_tags(limit=5, query=None):
    """
    {% load post_tags %}
    {% popular_tags as popular_tags_list %}
    {% for tag in popular_tags_list %}
      <a href="{% url 'posts_tagged' slug=tag.slug %}">
        {{ tag.tag.title }} <span class="badge">{{ tag.total }}</span>
      </a>
    {% endfor %}

    used in:
        - app_blog/posts_list.html
    """
    tags_queryset = Tag.objects.all()
    if query:
        tags_queryset = Tag.objects.filter(Q(title__startswith=query))

    mapping = [
        {
            'tag': tag,
            'total': Post.objects.published().filter(tags__slug=tag.slug).count()
        } for tag in tags_queryset
    ]
    mapping.sort(key=lambda x: int(x['total']), reverse=True)
    return mapping[:limit]


@register.simple_tag
def hot_posts(limit=5):
    """
    {% load post_tags %}
    {% hot_posts as hot_posts_list %}
    {% for post in hot_posts_list %}
      <a href="{% url 'posts_detail' slug=post.slug %}">{{ post.title }}</a>
    {% endfor %}

    used in:
        - app_blog/posts_list.html
    """
    queryset = Post.objects.published().order_by('-rating_likes')
    top_posts = Visitor.objects.filter(post__in=queryset).values('post')\
        .annotate(total=Count('post__pk')).order_by('-total')
    id_top_posts = [pk['post'] for pk in top_posts]
    filter_posts = list(queryset.filter(pk__in=id_top_posts,
                                        modified__month=timezone.now().month,
                                        modified__year=timezone.now().year))
    queryset = sorted(filter_posts, key=lambda i: id_top_posts.index(i.pk))
    return queryset[:limit]


@register.simple_tag
def random_posts(limit=5):
    """
    {% load post_tags %}
    {% random_posts as random_posts_list %}
    {% for post in random_posts_list %}
      <a href="{% url 'posts_detail' slug=post.slug %}">{{ post.title }}</a>
    {% endfor %}

    used in:
        - app_blog/posts_list.html
    """
    return Post.objects.published().order_by('-rating_likes').order_by('?')[:limit]
