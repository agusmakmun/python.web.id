# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db.models import (Q, Count)
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView, UpdateView,
                                  FormView, TemplateView)

from apps.blog.models.tag import Tag
from apps.blog.models.post import (Post, Page)


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
        # return Post.objects.filter(tags=self.tag).published()
        return self.tag.post_set.published()

    @property
    def extra_context(self):
        return dict(tag=self.tag)
