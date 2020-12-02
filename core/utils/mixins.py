# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin


class SuperUserLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
