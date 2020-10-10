# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_auth.views import (LogoutView, UserDetailsView, PasswordResetView)

from apps.api.versioned.v1.serializers.auth import (
    PasswordResetSerializer, UserDetailsSerializer
)


class LoginView(ObtainAuthToken):
    """ Class View to handle the Login Token Authentication """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, __ = Token.objects.get_or_create(user=user)
        token.created = timezone.now()  # updating new session
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
        return Response(content, status=content.get('status'))


class UserDetailsView(UserDetailsView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer


class PasswordResetView(PasswordResetView):
    """
    [THIS CLASS VIEWS IS DOESN'T USED YET]

    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: `email`
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """
        curl --location --request POST "{{url}}/api/v1/auth/password/reset/" \
             --header 'Response-Format: application/json' \
             --header "Content-Type: application/json" \
             --header "Accept-Language: en" \
             --data "{
                  \"email\": \"foobar@gmail.com\"
               }"
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        content = {'status': status.HTTP_200_OK,
                   'message': _('Password reset email has been sent.')}
        return Response(content, status=content.get('status'))
