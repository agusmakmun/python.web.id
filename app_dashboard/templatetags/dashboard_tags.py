# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils import timezone
from django.db.models import (Q, Count)
from django.contrib.auth.models import User

from app_blog.models import (Post, Tag, Visitor, Gallery)

register = template.Library()


@register.simple_tag
def get_total_tags_this_year():
    """
    {% load post_tags %}
    {% get_total_tags_this_year %}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Tag.objects.filter(created__year=timezone.now().year).count()


@register.filter
def get_total_tags_this_month(month):
    """
    {% load post_tags %}
    {{ 1|get_total_tags_this_month }}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Tag.objects.filter(
        created__year=timezone.now().year,
        created__month=month
    ).all().count()


@register.simple_tag
def get_total_posts_this_year():
    """
    {% load post_tags %}
    {% get_total_posts_this_year %}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Post.objects.filter(created__year=timezone.now().year).published().count()


@register.filter
def get_total_posts_this_month(month):
    """
    {% load post_tags %}
    {{ 1|get_total_posts_this_month }}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Post.objects.filter(
        created__year=timezone.now().year,
        created__month=month
    ).published().count()


@register.simple_tag
def get_total_users_this_year():
    """
    {% load post_tags %}
    {% get_total_users_this_year %}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return User.objects.filter(date_joined__year=timezone.now().year).all().count()


@register.filter
def get_total_users_this_month(month):
    """
    {% load post_tags %}
    {{ 1|get_total_users_this_month }}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return User.objects.filter(
        date_joined__year=timezone.now().year,
        date_joined__month=month
    ).all().count()


@register.simple_tag
def get_total_galleries_this_year():
    """
    {% load post_tags %}
    {% get_total_galleries_this_year %}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Gallery.objects.filter(created__year=timezone.now().year).all().count()


@register.filter
def get_total_galleries_this_month(month):
    """
    {% load post_tags %}
    {{ 1|get_total_galleries_this_month }}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Gallery.objects.filter(
        created__year=timezone.now().year,
        created__month=month
    ).all().count()


@register.simple_tag
def get_total_visitors_this_year():
    """
    {% load post_tags %}
    {% get_total_visitors_this_year %}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Visitor.objects.filter(created__year=timezone.now().year).all().count()


@register.filter
def get_total_visitors_this_month(month):
    """
    {% load post_tags %}
    {{ 1|get_total_visitors_this_month }}

    used in:
        - app_dashboard/dashboard_home.html
    """
    return Visitor.objects.filter(
        created__year=timezone.now().year,
        created__month=month
    ).all().count()
