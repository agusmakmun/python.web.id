# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer as PasswordResetSerializerDefault


class PasswordResetSerializer(PasswordResetSerializerDefault):
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
