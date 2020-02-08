# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (TemplateView, DetailView)
from django.views.generic.base import RedirectView

from app_blog.models import Page


class DocumentationHome(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('docs_detail', kwargs={'slug': 'introduction'})


class DocumentationDetail(DetailView):
    context_object_name = 'documentation'
    template_name = 'app_api/docs/docs_page.html'

    def get_object(self):
        return get_object_or_404(Page, slug=self.kwargs['slug'], status='documentation')
