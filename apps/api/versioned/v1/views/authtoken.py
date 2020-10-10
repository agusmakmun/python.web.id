# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout as django_logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_auth.views import (LoginView, LogoutView, UserDetailsView,
                             PasswordResetView, PasswordResetConfirmView,
                             PasswordChangeView)
from rest_auth.registration.app_settings import register_permission_classes


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        token.created = timezone.now() # updating new session
        token.save()

        expiration_days = getattr(settings, 'REST_FRAMEWORK_AUTH_EXPIRATION_DAYS', 365)
        expiration_date = timezone.now() + timezone.timedelta(days=expiration_days)

        response = {
            'success': True,
            'result': {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'expiration_date': expiration_date
            }
        }
        return Response(response)


class LogoutView(LogoutView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    def logout(self, request):
        """
        curl --location --request POST '{{url}}/api/v1/auth/logout/' \
             --header 'Authorization: Token {{token_auth}}' \
             --header 'Response-Format: application/json' \
             --header 'Accept-Language: id'
        """
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        content = {'status': status.HTTP_200_OK,
                   'message': _('Successfully logout.')}
        response = Response(content, status=content.get('status'))

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response


# class PasswordResetView(PasswordResetView):
#     """
#     Calls Django Auth PasswordResetForm save method.
#
#     Accepts the following POST parameters: `email`
#     Returns the success/fail message.
#     """
#     serializer_class = PasswordResetSerializer
#
#     def post(self, request, *args, **kwargs):
#         """
#         curl --location --request POST "{{url}}/api/v1/account/rest-auth/password/reset/" \
#              --header "Content-Type: application/json" \
#              --header 'Response-Format: application/json' \
#              --header "Accept-Language: id" \
#              --data "{
#                   \"email\": \"summoss@gmail.com\"
#                }"
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         content = {'status': status.HTTP_200_OK,
#                    'message': _("Email atur ulang kata sandi telah dikirim.")}
#         return Response(content, status=content.get('status'))
#
#
# class PasswordResetConfirmView(PasswordResetConfirmView):
#     """
#     Password reset e-mail link is confirmed, therefore
#     this resets the user's password.
#
#     Accepts the following POST parameters:
#         `token`, `uid`,
#         `new_password1`, `new_password2`
#     Returns the success/fail message.
#     """
#
#     def post(self, request, *args, **kwargs):
#         """
#         curl --location --request POST "{{url}}/api/v1/account/rest-auth/password/reset/confirm/" \
#              --header "Content-Type: application/json" \
#              --header 'Response-Format: application/json' \
#              --header "Accept-Language: id" \
#              --data "{
#                   \"uid\": \"OA\",
#                   \"token\": \"57q-cbb39067d8afd17c92a1\",
#                   \"new_password1\": \"agus12345\",
#                   \"new_password2\": \"agus12345\"
#                }"
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         content = {'status': status.HTTP_200_OK,
#                    'message': _("Kata sandi telah diatur ulang dengan kata sandi baru.")}
#         return Response(content, status=content.get('status'))
#
#
# class PasswordChangeView(PasswordChangeView):
#     """
#     Calls Django Auth SetPasswordForm save method.
#     Accepts the following POST parameters: `new_password1`, `new_password2`
#     Returns the success/fail message.
#     """
#
#     def post(self, request, *args, **kwargs):
#         """
#         curl --location --request POST "{{url}}/api/v1/account/rest-auth/password/reset/change/" \
#              --header "Authorization: Token 3445dd11d400df18cfe3d80cdb7ee7189a7087ad" \
#              --header "Content-Type: application/json" \
#              --header 'Response-Format: application/json' \
#              --header "Accept-Language: id" \
#              --data "{
#                   \"old_password\": \"agus12345\",
#                   \"new_password1\": \"agus12345\",
#                   \"new_password2\": \"agus12345\"
#                }"
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         content = {'status': status.HTTP_200_OK,
#                    'message': _("Kata sandi baru telah disimpan.")}
#         return Response(content, status=content.get('status'))
