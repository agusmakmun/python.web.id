# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from martor.widgets import AdminMartorWidget

from apps.blog.models.post import Post
from apps.blog.utils.slug import generate_unique_slug


class PostForm(forms.ModelForm):

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = generate_unique_slug(self.Meta.model, instance.title, instance)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Post
        fields = ('title', 'description', 'tags',
                  'keywords', 'meta_description', 'publish')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control text-normal'}),
            'description': AdminMartorWidget(),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control text-normal'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control text-normal'}),
            'meta_description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control text-normal'}),
            'publish': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }
