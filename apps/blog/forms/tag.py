# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.tag import Tag


class TagForm(forms.ModelForm):

    def clean_name(self):
        name = slugify(self.cleaned_data['name'])
        if Tag.objects.filter(name=name):
            raise forms.ValidationError(_('%(tag)s already exist!') % {'tag': name})
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = slugify(self.clean_name())
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Tag
        fields = ('name', 'description')
