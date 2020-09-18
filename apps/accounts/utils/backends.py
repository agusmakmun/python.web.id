# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import (backends, get_user_model)
from django.db.models import Q


class CustomAuthBackend(backends.ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(Q(username=username) |
                                    Q(email__iexact=username))
            if getattr(user, 'is_active', True) and user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
        return None
