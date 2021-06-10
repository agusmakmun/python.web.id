# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from martor.fields import MartorFormField


class MartorDemoForm(forms.Form):
    description = MartorFormField()
