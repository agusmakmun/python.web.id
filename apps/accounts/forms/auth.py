# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from allauth.account.forms import (
    LoginForm, SignupForm,
    ResetPasswordForm, ResetPasswordKeyForm
)

User = get_user_model()


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


class LoginForm(LoginForm):
    """
    Login form for users.
    This form extented from `allauth.account.forms.LoginForm`
    And updating the form for google `captcha`.
    """
    error_message = {
        'username_not_exist': _("User is not registered!")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
                # 'style': ('transform:scale(1.057);-webkit-transform:scale(1.057);'
                #           'transform-origin:0 0;-webkit-transform-origin:0 0;')
            }
        ))

    def clean_login(self):
        username = self.cleaned_data.get('login')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_message['username_not_exist'],
                code='username_not_exist',
            )
        return username


class SignUpForm(SignupForm):
    """
    Sign up form for users.
    This form extented from `allauth.account.forms.SignupForm`
    And updating the form for google `captcha` and some validators.
    """
    exceptor_usernames = [
        'admin', 'administrator', 'moderator',
        'test', 'testing', 'tester', 'user',
        'root', 'password', 'presiden', 'president',
        'anon', 'anonymous', 'dancok', 'jancuk',
        'xx', 'xxx', 'xxxx', 'xxxxx', 'xxxxxx'
    ]
    error_message = {
        'username_misspace': _("Username with white space forbidden to use!"),
        'username_forbidden': _("This username forbidden to use!"),
        'email_exist': _("E-mail already exist, please use another email!"),
        'password_mismatch': _("The two password didn't match."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    email = forms.EmailField(label=_('E-mail'), required=True,
                             widget=forms.EmailInput(attrs={'placeholder': _('E-mail')}))

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
                # 'style': ('transform:scale(1.057);-webkit-transform:scale(1.057);'
                #           'transform-origin:0 0;-webkit-transform-origin:0 0;')
            }
        ))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise forms.ValidationError(
                self.error_message['username_misspace'],
                code='username_misspace',
            )
        elif username in self.exceptor_usernames \
                or username.startswith('test') \
                or username.startswith('admin'):
            raise forms.ValidationError(
                self.error_message['username_forbidden'],
                code='username_forbidden',
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in [u.email for u in User.objects.all()]:
            raise forms.ValidationError(
                self.error_message['email_exist'],
                code='email_exist',
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_message['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class ResetPasswordForm(ResetPasswordForm):
    """
    Reset password form for users.
    This form extented from `allauth.account.forms.ResetPasswordForm`
    And updating the form for google `captcha`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
                # 'style': ('transform:scale(1.057);-webkit-transform:scale(1.057);'
                #           'transform-origin:0 0;-webkit-transform-origin:0 0;')
            }
        ))


class ResetPasswordKeyForm(ResetPasswordKeyForm):
    """
    Reset password from key form for users.
    This form extented from `allauth.account.forms.ResetPasswordKeyForm`
    And updating some validators.
    """
    error_message = {
        'password_mismatch': _("The two password didn't match."),
        'password_misspace': _("Password with space forbidden to use.")
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_message['password_mismatch'],
                code='password_mismatch',
            )
        if ' ' in password2:
            raise forms.ValidationError(
                self.error_message['password_misspace'],
                code='password_misspace',
            )
        return password2
