# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))
    sender = forms.CharField(label=_('Sender'), max_length=20)
    subject = forms.CharField(label=_('Subject'), max_length=100)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
                # 'style': ('transform:scale(1.057);-webkit-transform:scale(1.057);'
                #           'transform-origin:0 0;-webkit-transform-origin:0 0;')
            }
        ))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

        # use the selection email when user has logged in
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'emailaddress_set'):
                emails = user.emailaddress_set.values_list('email', 'email')
                if emails.exists():
                    self.fields['email'] = forms.ChoiceField(label=_('E-mail'), choices=emails)

            # setting up the sender
            self.fields['sender'].initial = self.request.user

            # deleting the captcha
            if 'captcha' in self.fields:
                del self.fields['captcha']

        # updating the html class
        for (k, v) in self.fields.items():
            attrs = {'class': 'form-control text-normal'}
            if k == 'message':
                attrs.update({'rows': 5})

            self.fields[k].widget.attrs = attrs
