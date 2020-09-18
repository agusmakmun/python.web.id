# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db.models import (Q, Count)
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView, UpdateView,
                                  FormView, TemplateView)

from updown.models import Vote

from apps.blog.models.tag import Tag
from apps.blog.models.post import (Post, Page)
from apps.accounts.models.user import User


class PostListView(ListView):
    paginate_by = getattr(settings, 'DEFAULT_PAGINATION_NUMBER', 10)
    template_name = 'apps/blog/post/list.html'
    queryset = Post.objects.published()
    context_object_name = 'posts'

    def get_default_queryset(self):
        """ need this to implement overwrite the default queryset """
        return self.queryset

    @property
    def extra_context(self):
        """ additional `context_data` for `get_context_data` """
        return None

    def get_queryset(self):
        queryset = self.get_default_queryset()
        self.query = self.request.GET.get('q')

        if self.query:
            queryset = queryset.filter(
                Q(title__iexact=self.query) | Q(title__icontains=self.query) |
                Q(description__iexact=self.query) | Q(description__icontains=self.query) |
                Q(keywords__iexact=self.query) | Q(keywords__icontains=self.query)
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['query'] = self.query
        if self.extra_context:
            context_data.update(**self.extra_context)
        return context_data


class PostListTaggedView(PostListView):
    template_name = 'apps/blog/post/tagged.html'

    def get_default_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return self.tag.post_set.published()

    @property
    def extra_context(self):
        return dict(tag=self.tag)


class PostListAuthorView(PostListView):
    template_name = 'apps/blog/post/author.html'

    def get_default_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return self.author.post_set.published()

    @property
    def extra_context(self):
        return dict(author=self.author)


class PostDetailView(DetailView):
    template_name = 'apps/blog/post/detail.html'
    context_object_name = 'post'
    model = Post

    def get_related_posts(self, limit=5):
        """
        function to get the related posts.
        :param `limit` is integer limit of total posts.
        :return posts object
        """
        queries = {'tags__in': self.object.tags.all()}
        return self.model.objects.published()\
                                 .filter(**queries)\
                                 .exclude(id=self.object.id)\
                                 .distinct()[:limit]

    @property
    def user_post_vote(self):
        """
        to check whenever user is voted the post.
        {% if user_post_vote %}orange{% else %}grey{% endif %}
        """
        return self.object.rating.get_rating_for_user(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['related_posts'] = self.get_related_posts(limit=5)
        context_data['user_post_vote'] = self.user_post_vote
        return context_data
