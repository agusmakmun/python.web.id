# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import (path, include)

urlpatterns = [
    path('v1/', include('apps.api.versioned.v1.urls')),
]
