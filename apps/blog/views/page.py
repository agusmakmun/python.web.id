# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import (get_object_or_404, redirect)
from django.utils.translation import gettext_lazy as _
from django.views.generic import (TemplateView, FormView)

from apps.blog.models.post import Page
from apps.blog.forms.contact import ContactForm
from apps.blog.forms.martor import MartorDemoForm


class BasePageDetailView(TemplateView):
    """ base class to show the detail of page """
    template_name = 'apps/blog/page/detail.html'
    content_path = None
    page_title = None

    def get_content(self):
        """ function to read the markdown content """
        file_path = os.path.join(settings.BASE_DIR, self.content_path)
        if os.path.exists(file_path):
            return open(file_path, 'r').read()
        return ''

    @property
    def extra_context(self):
        """ additional `context_data` for `get_context_data` """
        return None

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['page_title'] = self.page_title
        context_data['content'] = self.get_content()
        if self.extra_context:
            context_data.update(**self.extra_context)
        return context_data


class PageAboutView(BasePageDetailView):
    content_path = '.ext/pages/about.md'
    page_title = _('About')


class PageDevelopersView(BasePageDetailView):
    content_path = '.ext/pages/developers.md'
    page_title = _('Developers')


class PageDisclaimerView(BasePageDetailView):
    content_path = '.ext/pages/disclaimer.md'
    page_title = _('Disclaimer')


class PagePrivacyPolicyView(BasePageDetailView):
    content_path = '.ext/pages/privacy-policy.md'
    page_title = _('Privacy Policy')


class PageServicesView(BasePageDetailView):
    content_path = '.ext/pages/services.md'
    page_title = _('Services')


class PageSponsorView(BasePageDetailView):
    content_path = '.ext/pages/sponsor.md'
    page_title = _('Sponsor')


class PageTOSView(BasePageDetailView):
    content_path = '.ext/pages/terms-of-service.md'
    page_title = _('Terms of Service')


class PageFromDatabaseView(BasePageDetailView):

    def get_object(self):
        slug = self.kwargs['slug']
        self.object = get_object_or_404(Page, slug=slug)
        self.page_title = self.object.title
        return self.object

    def get_content(self):
        return self.object.description

    @property
    def extra_context(self):
        """ additional `context_data` for `get_context_data` """
        return {'page': self.object}


class ContactUsView(FormView):
    template_name = 'apps/blog/page/contact.html'
    form_class = ContactForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        sender = form.cleaned_data['sender']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['email']

        try:
            subject_new = _('%(subject)s from %(email)s by %(sender)s')
            subject_new = subject_new % {'subject': subject, 'email': from_email, 'sender': sender}
            recipients = [settings.EMAIL_HOST_USER]

            send_mail(subject_new, message, from_email, recipients)
            messages.success(self.request, _('Your message successfully sended!'))
            return redirect(reverse('apps.blog:post_list'))

        except Exception as error:
            messages.error(self.request, error)

        return redirect(reverse('apps.blog:page_contact_us'))


class MartorDemoView(FormView):
    template_name = 'apps/blog/page/martor_demo.html'
    form_class = MartorDemoForm
