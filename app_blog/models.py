# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
# from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from updown.models import Vote
from updown.fields import RatingField
from martor.models import MartorField
from app_blog.utils.slug import generate_unique_slug
from app_user.models import Profile


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Tag(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)

    def __str__(self):
        return self.title

    def get_posts(self):
        return Post.objects.filter(tags=self).published()

    @property
    def total_posts(self):
        return self.get_posts().count()

    def save(self, *args, **kwargs):
        if not self.pk:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Detail Tag')
        verbose_name_plural = _('Tags')
        ordering = ['-created']


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(publish=True)

    def unpublished(self):
        return self.filter(publish=False)


@python_2_unicode_compatible
class Post(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = MartorField(_('Description'))
    tags = models.ManyToManyField('Tag')
    keywords = models.CharField(_('Keywords'), null=True, blank=True,
                                max_length=200, help_text=_('Keywords sparate by comma.'))
    meta_description = models.TextField(_('Meta Description'), null=True, blank=True)
    is_featured = models.BooleanField(_('Is Featured?'), default=False)
    publish = models.BooleanField(_('Publish'), default=True)
    rating = RatingField(can_change_vote=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    # @models.permalink
    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'slug': self.slug})

    def get_visitors(self):
        return Visitor.objects.filter(post=self)

    @property
    def total_visitors(self):
        return self.get_visitors().count()

    def get_favorites(self):
        return Favorite.objects.filter(post=self)

    @property
    def total_favorites(self):
        return self.get_favorites().count()

    def save(self, *args, **kwargs):
        """ generate an unique slug """
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        else:  # create
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ run delete action for instanced objects """
        Visitor.objects.filter(post=self).delete()
        Favorite.objects.filter(post=self).delete()
        Vote.objects.filter(content_type__model='post',
                            object_id=self.id).delete()
        super(Post, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Detail Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created']


class PageQuerySet(models.QuerySet):

    def published(self):
        return self.filter(publish=True)

    def unpublished(self):
        return self.filter(publish=False)


@python_2_unicode_compatible
class Page(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = MartorField(_('Description'))
    STATUS_CHOICES = (
        ('site', _('Site')),
        ('private', _('Private')),
        ('documentation', _('Documentation'))
    )
    status = models.CharField(_('Status'), max_length=20,
                              choices=STATUS_CHOICES, default='site')
    publish = models.BooleanField(_('Publish'), default=True)
    objects = PageQuerySet.as_manager()

    def __str__(self):
        return self.title

    # this will give an error in /admin
    # @models.permalink
    # def get_absolute_url(self):
    #    return reverse("page_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Page, self.title)
        else:  # create
            self.slug = generate_unique_slug(Page, self.title)
        super(Page, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Detail Page')
        verbose_name_plural = _('Pages')
        ordering = ['-created']


@python_2_unicode_compatible
class Visitor(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.CharField(_('IP Address'), max_length=40)

    def __str__(self):
        title = self.post.title
        title = title if len(title) <= 50 else '%s ...' % title[:50]
        return _('%(ip)s visited %(post)s') % {'ip': self.ip, 'post': title}

    class Meta:
        verbose_name = _('Detail Visitor')
        verbose_name_plural = _('Visitors')
        ordering = ['-created']


@python_2_unicode_compatible
class Favorite(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        title = self.post.title
        title = title if len(title) <= 50 else '%s ...' % title[:50]
        return _('%(post)s marked as favorite by %(user)s') % {'post': title, 'user': self.user}

    class Meta:
        # unique_together = ('user', 'post')
        verbose_name = _('Detail Favorite')
        verbose_name_plural = _('Favorites')
        ordering = ['-created']


@python_2_unicode_compatible
class Gallery(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    attachment = models.FileField(_('Attachment'), upload_to='attachments/%Y/%m/%d')

    def __str__(self):
        return self.title or self.attachment.name.split('/')[-1]

    class Meta:
        verbose_name = _('Detail Gallery')
        verbose_name_plural = _('Galleries')
        ordering = ['-created']
