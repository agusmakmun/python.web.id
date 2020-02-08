# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from nocaptcha_recaptcha.fields import NoReCaptchaField
from allauth.account.forms import (LoginForm, SignupForm,
                                   ResetPasswordForm, ResetPasswordKeyForm)
from app_user.models import Profile


class LoginForm(LoginForm):
    """
    Login form for users.
    This form extented from `allauth.account.forms.LoginForm`
    And updating the form for google `captcha`.
    """
    error_message = {
        'username_not_exist': _("User is not registered!")
    }

    def clean_login(self):
        username = self.cleaned_data.get('login')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_message['username_not_exist'],
                code='username_not_exist',
            )
        return username

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.fields['captcha'] = NoReCaptchaField()


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
        'xx', 'xxx',  'xxxx', 'xxxxx', 'xxxxxx'
    ]
    error_message = {
        'username_misspace': _("Username with white space forbidden to use!"),
        'username_forbidden': _("This username forbidden to use!"),
        'email_exist': _("Email already exist, please use another email!"),
        'password_mismatch': _("The two password didn't match."),
    }

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

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.fields['captcha'] = NoReCaptchaField()
        self.fields['email'] = forms.EmailField(
            label=_('Email'), required=True,
            widget=forms.EmailInput(attrs={'placeholder': _('Email')}))


class ResetPasswordForm(ResetPasswordForm):
    """
    Reset password form for users.
    This form extented from `allauth.account.forms.ResetPasswordForm`
    And updating the form for google `captcha`.
    """

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.fields['captcha'] = NoReCaptchaField()


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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)


class SendEmailForm(forms.Form):
    """
    Send email form for user/member.
    to send an email to another member.
    """
    subject = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.TextInput())


class ProfileForm(forms.ModelForm):
    """
    Profile form
    """
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', ]
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': _('City, Country')}),
            'about_me': forms.Textarea(attrs={'rows': 5, 'placeholder': _('Tell us about you ...')}),
            'birth_date': forms.DateInput(attrs={'class': 'ui calendar', 'placeholder': 'yyyy-mm-dd'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://python.web.id'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'https://twitter.com/username'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username'})
        }
