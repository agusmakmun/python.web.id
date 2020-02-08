# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(_('Display name'), max_length=200, null=True, blank=True)
    location = models.CharField(_('Location'), max_length=200, null=True, blank=True)
    about_me = models.TextField(_('About Me'), null=True, blank=True)
    website = models.URLField(_('Website'), blank=True, null=True)
    twitter = models.URLField(_('Twitter'), null=True, blank=True)
    linkedin = models.URLField(_('Linkedin'), null=True, blank=True)
    github = models.URLField(_('Github'), null=True, blank=True)
    birth_date = models.DateField(_('Birth date'), null=True, blank=True)

    def get_user_posts(self):
        return self.user.post_set.published()

    @property
    def total_posts(self):
        return self.get_user_posts().count()

    @property
    def total_featured_posts(self):
        return self.get_user_posts().filter(is_featured=True).count()

    @property
    def total_favorites(self):
        return self.user.favorite_set.all().count()

    def __str__(self):
        name = self.display_name
        return '%s' % name if name else self.user.username

    def get_absolute_url(self):
        return reverse('author_posts_page',
                       kwargs={'username': self.user.username})

    class Meta:
        verbose_name = _('Detail Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-user__date_joined']
