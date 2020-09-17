# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class AuthAdminForm(AuthenticationForm):

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
                # 'style': ('transform:scale(1.057);-webkit-transform:scale(1.057);'
                #           'transform-origin:0 0;-webkit-transform-origin:0 0;')
            }
        ))
