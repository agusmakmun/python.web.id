# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.tag import Tag
from apps.blog.forms.tag import TagForm


class TagListView(FormMixin, ListView):
    template_name = 'apps/blog/tag/list.html'
    queryset = Tag.objects.published()
    context_object_name = 'tags'
    form_class = TagForm
    paginate_by = 16

    def get_queryset(self):
        queryset = self.queryset
        self.sort = self.request.GET.get('sort', 'popular')
        self.query = self.request.GET.get('q')

        if self.query:
            queryset = queryset.filter(name__icontains=self.query)
        if self.sort == 'name':
            return queryset.order_by('name')
        elif self.sort == 'new':
            return queryset.order_by('-created_at')
        return queryset.annotate(total=Count('post')).order_by('-total')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You must login to create the tag!'))
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, _('Tag successfully created!'))
            else:
                messages.error(request, _('Tag failed to save!'))
        return redirect(reverse('apps.blog:tag_list'))

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['query'] = self.query
        context_data['sort'] = self.sort
        return context_data
