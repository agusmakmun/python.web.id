# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _


class PageDetailView(TemplateView):
    template_name = 'apps/blog/page/detail.html'
    content_path = None
    page_title = None

    def get_content(self):
        """ function to read the markdown content """
        file_path = os.path.join(settings.BASE_DIR, self.content_path)
        if os.path.exists(file_path):
            return open(file_path, 'r').read()
        return ''

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['page_title'] = self.page_title
        context_data['content'] = self.get_content()
        return context_data


class PageAboutView(PageDetailView):
    content_path = '.ext/pages/about.md'
    page_title = _('About')


class PageDisclaimerView(PageDetailView):
    content_path = '.ext/pages/disclaimer.md'
    page_title = _('Disclaimer')


class PagePrivacyPolicyView(PageDetailView):
    content_path = '.ext/pages/privacy-policy.md'
    page_title = _('Privacy Policy')


class PageServiceView(PageDetailView):
    content_path = '.ext/pages/service.md'
    page_title = _('Service')


class PageTOSView(PageDetailView):
    content_path = '.ext/pages/terms-of-service.md'
    page_title = _('Terms of Service')
