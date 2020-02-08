# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from nocaptcha_recaptcha.fields import NoReCaptchaField
from martor.widgets import AdminMartorWidget

from app_blog.models import (Post, Tag, Page)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'tags',
                  'keywords', 'meta_description', 'publish']
        widgets = {
            'description': AdminMartorWidget(),
            'tags': forms.SelectMultiple(attrs={'class': 'ui search fluid dropdown tags-dropdown'}),
            'keywords': forms.TextInput(attrs={'placeholder': _('Separate by comma (,)')}),
            'meta_description': forms.Textarea(attrs={'rows': 2})
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        if Tag.objects.filter(slug=slug):
            raise ValidationError(_('%(tag)s already exist!') % {'tag': title})
        return title

    def save(self, commit=True):
        instance = super(TagForm, self).save(commit=False)
        instance.slug = slugify(self.clean_title())
        if commit:
            instance.save()
        return instance


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'description', 'status', 'publish']
        widgets = {'description': AdminMartorWidget()}


class ContactForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    sender = forms.CharField(label=_('Sender'), max_length=20)
    subject = forms.CharField(label=_('Subject'), max_length=100)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)
    captcha = NoReCaptchaField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ContactForm, self).__init__(*args, **kwargs)

        if self.request.user.is_authenticated:
            emails = self.request.user.emailaddress_set.values_list('email', 'email')
            if emails.exists():
                self.fields['email'] = forms.ChoiceField(label=_('Email'), choices=emails)
            self.fields['sender'].initial = self.request.user
            del self.fields['captcha']
