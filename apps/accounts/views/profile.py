# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, UpdateView, DetailView)

from apps.accounts.models.user import (User, Profile)


class ProfileDetailView(DetailView):
    template_name = 'apps/accounts/user/profile.html'
    context_object_name = 'profile'
    widget_list_limit = 5

    def get_object(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        profile, truefalse = Profile.objects.get_or_create(user=self.user)
        return profile

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['posts'] = self.author_posts()[:self.widget_list_limit]
        # context_data['total_posts'] = self.author_posts().count()
        # context_data['favorites'] = self.get_favorites()[:self.widget_list_limit]
        # context_data['total_favorites'] = self.get_favorites().count()
        # context_data['tags'] = self.get_tags()[:10]
        # context_data['total_tags'] = len(self.get_tags())
        # context_data['votes'] = self.get_votes()
        # context_data['total_votes'] = self.get_votes().count()
        # context_data['total_votes_up'] = self.get_votes(mode='up').count()
        # context_data['total_votes_down'] = self.get_votes(mode='down').count()
        context_data['user'] = self.user
        return context_data
