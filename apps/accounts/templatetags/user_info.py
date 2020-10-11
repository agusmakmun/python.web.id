# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from apps.accounts.models.user import Profile
from apps.blog.models.addons import Favorite
from apps.blog.models.post import Post

register = template.Library()


@register.filter
def get_display_name(user):
    # NOT USED YET
    """
    {{ requst.user|get_display_name }}
    """
    profile = Profile.objects.filter(user=user)
    if profile.exists():
        display_name = profile.first().display_name
        if display_name is not None:
            return display_name
    return user.username


@register.filter
def get_user_posts(user):
    """
    Return all posts contains with this user.
    :param `user` is user model instance.
    used in:
        - this file
    """
    return Post.objects.published().filter(author=user)


@register.filter
def get_total_posts(user):
    """
    Return total posts contains with this user.
    :param `user` is user model instance.
    used in:
        - app_user/users_list.html
    """
    return get_user_posts(user).count()


@register.filter
def get_total_ratings(user, mode='all'):
    """
    Return total posts contains with this user.
    :param `user` is user model instance.
    :param `mode` is filter type for 'all', 'likes', or 'dislikes'.
    used in:
        - app_user/users_list.html
        - app_user/profile_detail.html
    """
    user_posts = get_user_posts(user)
    total_likes = sum([t.rating.likes for t in user_posts])
    total_dislikes = sum([t.rating.dislikes for t in user_posts])

    if mode == 'likes':
        return total_likes
    elif mode == 'dislikes':
        return total_dislikes

    # return reputation score for user
    return total_likes - total_dislikes


@register.filter
def get_user_favorites(user):
    """
    Return total favorites contains with this user.
    :param `user` is user model instance.
    used in:
        - this file
    """
    return Favorite.objects.published().filter(user=user)


@register.filter
def get_total_favorites(user):
    """
    Return total favorites contains with this user.
    :param `user` is user model instance.
    used in:
        -
    """
    return get_user_favorites(user=user).count()


@register.filter
def total_featured_posts(user):
    """
    Return total featured posts contains with this user.
    :param `user` is user model instance.
    used in:
        - app_user/users_list.html
        - app_user/profile_detail.html
    """
    return get_user_posts(user).filter(is_featured=True).count()
