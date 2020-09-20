# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    extending from base `AbstractUser`
    to rewrite the `id` AutoField to `id` `BigAutoField`
    """
    id = models.BigAutoField(primary_key=True)

    @property
    def fullname(self):
        if hasattr(self, 'profile') and self.profile:
            display_name = self.profile.display_name
            if display_name:
                return display_name
        return self.get_full_name() or self.username


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(_('Display name'), max_length=200, null=True, blank=True)
    location = models.CharField(_('Location'), max_length=200, null=True, blank=True)
    about_me = models.TextField(_('About Me'), null=True, blank=True)
    website = models.URLField(_('Website'), blank=True, null=True)
    github = models.URLField(_('Github'), null=True, blank=True)
    linkedin = models.URLField(_('Linkedin'), null=True, blank=True)
    instagram = models.URLField(_('Instagram'), null=True, blank=True)
    twitter = models.URLField(_('Twitter'), null=True, blank=True)
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
        return '%s' % name if name else self.user.fullname

    def get_absolute_url(self):
        kwargs = {'username': self.user.username}
        return reverse('apps.blog:post_list_author', kwargs=kwargs)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('-user__date_joined',)
