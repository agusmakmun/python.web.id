# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from apps.blog.models.addons import Visitor


def get_client_ip(request):
    """
    function to get the ip address from client.
    :param `request` is request object.
    :return string of client ip address.
    """
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip:
        ip = ip.split(', ')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def visitor_counter(request, content_type, object_id):
    """
    function to get/create the visitor,
    and count total visitors for current slug url.
    :param `request` is request object.
    :param `content_type` is content type object.
    :param `object_id` is integer object id.
    :return dict of {'client_ip': <str>, 'total_visitors': <int>}
    """
    client_ip = get_client_ip(request)
    visitor, tf = Visitor.objects.get_or_create(content_type=content_type,
                                                object_id=object_id,
                                                ip_address=client_ip)
    if tf or (not visitor.headers):
        visitor.headers = request.headers
        visitor.save()

    visitors = Visitor.objects.published()\
                              .filter(content_type=content_type,
                                      object_id=object_id)

    return dict(client_ip=client_ip, total_visitors=visitors.count())


def get_popular_objects(queryset, addon_model=Visitor, year=None):
    """
    function to get the popular queryset objects
    by counting the total visits.
    :param `queryset` is queryset objects, e.g: <QuerySet: ...>
    :param `addon_model` is optional class addons model, e.g: Visitor, Favorite
    :param `year` is optional integer to filter by specific year (default:None)
    :return list objects of the popular queryset.

    >>> from apps.blog.utils.visitor import get_popular_objects
    >>> from apps.blog.models.post import Post
    >>> queryset = Post.objects.published_public()
    >>> get_popular_objects(queryset)
    [<Post: NMD R1 Black and Blue Shoes>, <Post: Lorem ipsum>, ...]
    """
    model_class = queryset.model._meta.model
    content_type = ContentType.objects.get_for_model(model_class)

    if isinstance(year, int):
        queryset = queryset.filter(updated_at__year=year)

    object_ids = queryset.values_list('id', flat=True)
    object_ids_top = addon_model.objects.published()\
                                        .filter(content_type=content_type, object_id__in=object_ids)\
                                        .annotate(total=Count('object_id'))\
                                        .values_list('object_id', flat=True)\
                                        .order_by('-total')
    object_ids_top = list(object_ids_top)

    # method 1
    # queryset_includes = list(queryset.filter(id__in=object_ids_top))
    # queryset_includes.sort(key=lambda i: object_ids_top.index(i.id))

    # method 2
    queryset_includes = list(queryset.filter(id__in=object_ids_top))
    queryset = sorted(queryset_includes, key=lambda i: object_ids_top.index(i.pk))

    return queryset_includes
