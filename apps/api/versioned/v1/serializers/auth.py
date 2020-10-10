# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from rest_auth.app_settings import UserDetailsSerializer

User = get_user_model()


class PasswordResetSerializer(PasswordResetSerializer):
    email_template_name = 'apps/accounts/mail/registration/password_reset_email.html'
    html_email_template_name = 'apps/accounts/mail/registration/password_reset_email.html'

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'email_template_name': self.email_template_name,
            'html_email_template_name': self.html_email_template_name,
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'extra_email_context': {'url_password_reset': getattr(settings, 'URL_PASSWORD_RESET')},
            'use_https': request.is_secure(),
            'request': request
        }
        self.reset_form.save(**opts)


class UserDetailsSerializer(UserDetailsSerializer):
    groups = serializers.SerializerMethodField()

    def get_groups(self, user):
        return user.groups.values_list('name', flat=True)

    def to_representation(self, instance):
        user_data = super().to_representation(instance).copy()

        if 'pk' in user_data:
            user_data['id'] = user_data['pk']
            del user_data['pk']

        # display user token auth
        token_data = {}
        if hasattr(instance, 'auth_token'):
            expiration_days = getattr(settings, 'REST_FRAMEWORK_AUTH_EXPIRATION_DAYS', 365)
            expiration_date = timezone.now() + timezone.timedelta(days=expiration_days)
            token_data = model_to_dict(instance.auth_token, exclude=('user',))
            token_data['expiration_date'] = expiration_date

        # display user profile
        profile_data = {}
        if hasattr(instance, 'profile'):
            profile_data = model_to_dict(instance.profile, exclude=('user', 'id'))

        result = {'user': user_data, 'token': token_data, 'profile': profile_data}
        return {'result': result, 'status': 200, 'success': True, 'message': _('Success')}

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',
                  'first_name', 'last_name', 'last_login')
