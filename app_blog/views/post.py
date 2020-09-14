# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (Q, Count)
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView, UpdateView,
                                  FormView, TemplateView)

from app_blog.models.tag import Tag
from app_blog.models.post import (Post, Page)


class PostListView(ListView):
    template_name = 'app_blog/post/list.html'
    queryset = Post.objects.published()

    def get_queryset(self):
        queryset = self.queryset
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
        return context_data
