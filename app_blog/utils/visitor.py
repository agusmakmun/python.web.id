# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from app_blog.models.addons import Visitor


def get_client_ip(request):
    """ get ip address from client """
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip:
        ip = ip.split(', ')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def visitor_counter(request, post):
    """ to get/create the visitor, and count posts visitors """
    client_ip = get_client_ip(request)
    visitor, truefalse = Visitor.objects.get_or_create(post=post, ip=client_ip)
    visitor.save()
    visitors = Visitor.objects.filter(post=post).count()
    return dict(client_ip=client_ip, total_visitors=visitors)
