# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from app_blog.models import Gallery


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['title', 'attachment']

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['attachment'].widget = forms.FileInput()
