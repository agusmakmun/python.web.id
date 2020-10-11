# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models.user import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control text-normal', 'placeholder': _('Steve Jobs')}),
            'location': forms.TextInput(attrs={'class': 'form-control text-normal', 'placeholder': _('City, Country')}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control text-normal datepicker pl-2',  'placeholder': 'yyyy-mm-dd'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control text-normal', 'rows': 4, 'placeholder': _('Tell us about you ...')}),
            'website': forms.URLInput(attrs={'class': 'form-control text-normal', 'placeholder': 'https://python.web.id'}),
            'github': forms.URLInput(attrs={'class': 'form-control text-normal', 'placeholder': 'https://github.com/username'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control text-normal', 'placeholder': 'https://linkedin.com/in/username'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control text-normal', 'placeholder': 'https://instagram.com/username'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control text-normal', 'placeholder': 'https://twitter.com/username'}),
        }
