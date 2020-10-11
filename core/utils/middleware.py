# -*- coding: utf-8 -*-

import json
import copy

from django.conf import settings
from django.utils import (timezone, translation)
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

from sentry_sdk import capture_exception  # module

from rest_framework import status


class BaseAPIResponseMiddleware(MiddlewareMixin):

    def render_response(self, response):
        """
        function to fixed the response API following with this format:

        [1] success single
            {
             "status": 200,
             "success": true,
             "message": "The success message",
             "result": {}
            }

        [2] success list
            {
               "status": 200,
               "success": true,
               "message": null,
               "results": [],

               "count": 2,
               "page_size": 5,
               "current_page": 1,
               "next": "{{url}}/api/page/?page=2&search=a",
               "previous": null
            }

        [3] failed
            {
               "status": 400,
               "success": false,
               "message": "The failed message",
               "result": {}
            }
        """
        default_response_keys = ('status', 'status_http', 'detail', 'message',
                                 'success', 'non_field_errors', 'count',
                                 'page_size', 'current_page', 'next',
                                 'previous', 'result', 'results')
        response_data = copy.deepcopy(response.data)

        # setup default result if doesn't exist
        if not any(['result' in response_data, 'results' in response_data]):
            response_data.update({'result': {}})

        # setup default message into response data
        if 'message' not in response_data:
            response_data.update({'message': None})

        # store the status_code into response data
        if 'status' not in response_data:
            response_data.update({'status': response.status_code})

        # store the status_http into response data
        if 'status_http' not in response_data:
            response_data.update({'status_http': response.status_code})

        # updating the response message
        if 'detail' in response_data:
            response_data.update({'message': response_data.get('detail')})
            del response_data['detail']

        elif 'non_field_errors' in response_data:
            response_errors = '<br />'.join(response_data.get('non_field_errors'))
            response_data.update({'message': response_errors})
            del response_data['non_field_errors']

        # store the success boolean into response data
        if response.status_code >= 400:
            response_errors = []
            response_errors_keys = []

            for (key, value) in response_data.items():
                if key not in default_response_keys:
                    errors = ' '.join([str(v) for v in value])
                    errors = '%s: %s' % (key, errors)
                    response_errors.append(errors)
                    response_errors_keys.append(key)

            if len(response_errors) > 0:
                response_errors = '<br />'.join(response_errors)
                response_data.update({'message': response_errors})

            # deleting the errors in the field keys.
            if len(response_errors_keys) > 0:
                list(map(response_data.pop, response_errors_keys))

            if not response_data.get('message'):
                response_data.update({'message': _('Failed')})

            response_data.update({'success': False,
                                  'status_http': status.HTTP_200_OK})

        elif response.status_code >= 100:
            if not response_data.get('message'):
                response_data.update({'message': _('Success')})

            if 'success' not in response_data:
                response_data.update({'success': True})

        return response_data

    def process_response(self, request, response):
        if hasattr(response, 'data') and isinstance(response.data, dict):
            try:
                response_data = self.render_response(response)
                response.status_code = response_data.get('status_http')

                if 'status_http' in response_data:
                    del response_data['status_http']

                response.data = response_data
                response.content = json.dumps(response_data, cls=DjangoJSONEncoder)
            except Exception:
                pass

        # handle error response but without `response.data`
        # this error response specific for "Server Error" mode.
        response_format = request.headers.get('Response-Format')
        if (response.status_code >= 500) and (response_format == 'application/json'):
            # capturing the error message.
            capture_exception(str(response.content))

            response_data = {'success': False, 'result': {},
                             'status': response.status_code,
                             'message': response.reason_phrase}
            response.status_code = 200
            response.data = response_data
            response.content = json.dumps(response_data, cls=DjangoJSONEncoder)
            response['Content-Type'] = 'application/json'
        return response


class TokenExpirationMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if hasattr(request, 'auth') and request.auth:
            expiration_days = getattr(settings, 'REST_AUTH_EXPIRATION_DAYS', 365)
            expiration_date = timezone.now() - timezone.timedelta(days=expiration_days)
            is_expired = expiration_date > request.auth.created
            if is_expired:
                response_data = {'status': 401,
                                 'success': False,
                                 'message': _('Token already expired, please login '
                                              'with your username & password again!'),
                                 'result': {
                                     'key': request.auth.key,
                                     'expiration_date': str(expiration_date),
                                     'was_expired': True
                                 }}
                response.status_code = status.HTTP_200_OK
                response.content = json.dumps(response_data, cls=DjangoJSONEncoder)
                response.data = response_data
        return response
