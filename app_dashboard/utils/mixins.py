# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class SuperuserRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser:
            return HttpResponseRedirect('/')
        return super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
