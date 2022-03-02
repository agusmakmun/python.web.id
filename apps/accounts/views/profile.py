# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (UpdateView, DetailView)

from updown.models import Vote

from apps.blog.models.tag import Tag
from apps.blog.models.post import Post
from apps.blog.models.addons import Favorite
from apps.accounts.models.user import (User, Profile)
from apps.accounts.forms.profile import ProfileForm


class ProfileDetailView(DetailView):
    template_name = 'apps/accounts/user/profile.html'
    context_object_name = 'profile'
    widget_list_limit = 5

    def get_object(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        profile, truefalse = Profile.objects.get_or_create(user=self.user)
        return profile

    def default_queryset(self):
        return Post.objects.published().filter(author=self.user)

    def author_posts(self):
        posts = self.default_queryset()
        self.filter = self.request.GET.get('filter', 'votes')
        if self.filter == 'updates':
            posts = posts.order_by('-updated_at')
        elif self.filter == 'newest':
            posts = posts.order_by('-created_at')
        else:
            posts = posts.order_by('-rating_likes')
        return posts

    def get_favorites(self):
        return Favorite.objects.published().filter(user=self.user)

    def get_votes(self, mode='all'):
        votes = Vote.objects.filter(content_type__model='post', user=self.user)
        if mode == 'up':
            votes = votes.filter(score=1)
        elif mode == 'down':
            votes = votes.filter(score=-1)
        return votes

    def get_tags(self):
        posts = self.default_queryset()
        popular_tags = [
            {'tag': tag, 'total': posts.filter(tags=tag).count()}
            for tag in Tag.objects.published()
            if posts.filter(tags=tag).count() > 0
        ]
        popular_tags.sort(key=lambda x: int(x['total']), reverse=True)
        return popular_tags

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['posts'] = self.author_posts()[:self.widget_list_limit]
        context_data['total_posts'] = self.author_posts().count()
        context_data['favorites'] = self.get_favorites()[:self.widget_list_limit]
        context_data['total_favorites'] = self.get_favorites().count()
        context_data['tags_list'] = self.get_tags()[:10]
        context_data['total_tags'] = len(context_data['tags_list'])
        context_data['votes'] = self.get_votes()
        context_data['total_votes'] = context_data['votes'].count()
        context_data['total_votes_up'] = self.get_votes(mode='up').count()
        context_data['total_votes_down'] = self.get_votes(mode='down').count()
        context_data['user'] = self.user
        return context_data


class ProfileDetailActivityView(ProfileDetailView):
    template_name = 'apps/accounts/user/profile_activity.html'
    maximum_posts = 3

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['maximum_posts'] = self.maximum_posts
        return context_data


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'apps/accounts/user/profile_update.html'
    context_object_name = 'profile'
    form_class = ProfileForm
    model = Profile

    def get_success_url(self):
        return reverse('apps.accounts:profile_update')

    def get_object(self, queryset=None):
        profile, tf = self.model.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        messages.success(self.request, _('Profile successfully updated!'))
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        for field, _cls in self.form_class.base_fields.items():
            value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial
