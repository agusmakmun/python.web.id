# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from martor.widgets import AdminMartorWidget
from apps.product.models.product import Product


class ProductForm(forms.ModelForm):
    independent_fields = ('publish', 'long_description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (k, v) in self.fields.items():
            if k not in self.independent_fields:
                self.fields[k].widget.attrs = {'class': 'form-control text-normal'}

        self.fields['publish'].widget.attrs = {'class': 'custom-control-input'}
        self.fields['long_description'].widget = AdminMartorWidget()

    class Meta:
        model = Product
        exclude = ('author',)
