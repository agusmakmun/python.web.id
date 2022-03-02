# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import exception_handler


def handler400(request, exception=None):
    response = render(request, 'error_page.html',
                      {'title': _('400 Bad Request'), 'message': '400'})
    response.status_code = 400
    return response


def handler403(request, exception=None):
    response = render(request, 'error_page.html',
                      {'title': _('403 Permission Denied'), 'message': '403'})
    response.status_code = 403
    return response


def handler404(request, exception=None):
    response = render(request, 'error_page.html',
                      {'title': _('404 Not Found'), 'message': '404'})
    response.status_code = 404
    return response


def handler500(request, exception=None):
    response = render(request, 'error_page.html',
                      {'title': _('500 Server Error'), 'message': '500'})
    response.status_code = 500
    return response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status'] = response.status_code

    return response
