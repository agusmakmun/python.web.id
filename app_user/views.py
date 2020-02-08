# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, UpdateView, DetailView)
from django.contrib.auth.models import User
from django.db.models import (Q, Count, Sum)

from updown.models import Vote
from app_blog.models import (Tag, Post, Favorite)
from app_blog.utils.paginator import GenericPaginator
from app_user.forms import ProfileForm
from app_user.models import Profile


class UserList(GenericPaginator, ListView):
    template_name = 'app_user/users_list.html'
    paginate_by = 20

    def get_queryset(self):
        self.query = self.request.GET.get('q')
        self.abjad = self.request.GET.get('abjad')
        self.filter = self.request.GET.get('filter', '')

        users = User.objects.filter(is_active=True).order_by('-date_joined')
        posts = Post.objects.published()

        # return values of top users created the posts
        top_users_by_posts = posts.values('author__id').annotate(
            total=Count('id')).order_by('-total')

        # return values of top users created the posts by rating likes
        top_users_by_ratings = posts.values('author__id').annotate(
            rating=Sum('rating_likes')).order_by('-rating')

        if self.abjad:
            abjad_lowercase, abjad_uppercase = str(self.abjad).lower(), str(self.abjad).upper()
            users = users.filter(Q(username__startswith=abjad_lowercase) |
                                 Q(username__startswith=abjad_uppercase)).distinct()

        def sorted_users(values, by_query=False):
            """
            return sorted users from values by top posts, ratings, and comments
            """
            list_ids = [pk['author__id'] for pk in values]
            filter_users = list(users.filter(pk__in=list_ids))
            if by_query:
                filter_users = list(users.filter(pk__in=list_ids)
                                    .filter(Q(username__icontains=self.query) |
                                            Q(profile__display_name__icontains=self.query)))
            return sorted(filter_users, key=lambda i: list_ids.index(i.pk))

        if self.query and self.query != '':
            if self.filter == 'date_joined':
                self.filter = 'date_joined'
                users = users.filter(Q(username__icontains=self.query) |
                                     Q(profile__display_name__icontains=self.query)
                                     ).order_by('-date_joined').order_by('-id')
            elif self.filter == 'top_rated':
                self.filter = 'top_rated'
                users = sorted_users(values=top_users_by_ratings, by_query=True)
            else:
                self.filter = 'top_posts'
                users = sorted_users(values=top_users_by_posts, by_query=True)

        if self.filter == 'top_posts' and not self.query:
            self.filter = 'top_posts'
            users = sorted_users(values=top_users_by_posts, by_query=False)
        elif self.filter == 'top_rated' and not self.query:
            self.filter = 'top_rated'
            users = sorted_users(values=top_users_by_ratings, by_query=False)
        elif not self.query and not self.abjad:
            self.filter = 'date_joined'
            users = users.order_by('-date_joined').order_by('-id')

        return users

    def get_context_data(self, **kwargs):
        context_data = super(UserList, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['filter'] = self.filter
        context_data['abjad'] = self.abjad
        context_data['query'] = self.query
        return context_data


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'app_user/profile_edit.html'

    def get_success_url(self):
        return reverse('profile_edit')

    def get_object(self, queryset=None):
        profile, truefalse = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        messages.success(self.request, _('Profile updated!'))
        return super(ProfileEdit, self).form_valid(form)

    def get_initial(self):
        initial = super(ProfileEdit, self).get_initial()
        for field, _cls in self.form_class.base_fields.items():
            value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial


class ProfileDetail(DetailView):
    template_name = 'app_user/profile_detail.html'
    context_object_name = 'profile'
    widget_list_limit = 5

    def get_object(self, queryset=None):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        profile, truefalse = Profile.objects.get_or_create(user=self.user)
        return profile

    def default_queryset(self):
        return Post.objects.filter(author__username=self.kwargs['username']).published()

    def author_posts(self):
        posts = self.default_queryset()
        self.filter = self.request.GET.get('filter', 'votes')
        if self.filter == 'activity':
            posts = posts.order_by('-modified')
        elif self.filter == 'newest':
            posts = posts.order_by('-created')
        else:
            posts = posts.order_by('-rating_likes')
        return posts

    def get_favorites(self):
        return Favorite.objects.filter(user=self.user)

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
            for tag in Tag.objects.all()
            if posts.filter(tags=tag).count() > 0
        ]
        popular_tags.sort(key=lambda x: int(x['total']), reverse=True)
        return popular_tags

    def get_context_data(self, **kwargs):
        context_data = super(ProfileDetail, self).get_context_data(**kwargs)
        context_data['posts'] = self.author_posts()[:self.widget_list_limit]
        context_data['total_posts'] = self.author_posts().count()
        context_data['favorites'] = self.get_favorites()[:self.widget_list_limit]
        context_data['total_favorites'] = self.get_favorites().count()
        context_data['tags'] = self.get_tags()[:10]
        context_data['total_tags'] = len(self.get_tags())
        context_data['votes'] = self.get_votes()
        context_data['total_votes'] = self.get_votes().count()
        context_data['total_votes_up'] = self.get_votes(mode='up').count()
        context_data['total_votes_down'] = self.get_votes(mode='down').count()
        context_data['user'] = self.user
        return context_data


class ProfileDetailActivity(ProfileDetail):
    template_name = 'app_user/profile_detail_activity.html'
    maximum_posts = 20

    def get_context_data(self, **kwargs):
        context_data = super(ProfileDetail, self).get_context_data(**kwargs)
        context_data['maximum_posts'] = self.maximum_posts
        context_data['posts'] = self.author_posts()[:self.maximum_posts]
        context_data['total_posts'] = self.author_posts().count()
        context_data['favorites'] = self.get_favorites()
        context_data['total_favorites'] = self.get_favorites().count()
        context_data['tags'] = self.get_tags()
        context_data['total_tags'] = len(self.get_tags())
        context_data['votes'] = self.get_votes()
        context_data['total_votes'] = self.get_votes().count()
        context_data['total_votes_up'] = self.get_votes(mode='up').count()
        context_data['total_votes_down'] = self.get_votes(mode='down').count()
        context_data['user'] = self.user
        return context_data
