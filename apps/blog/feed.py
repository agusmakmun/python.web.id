# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from apps.blog.models.post import Post


class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'


class LatestPosts(Feed):
    feed_type = CorrectMimeTypeFeed

    title = 'Feed Blog Posts'
    link = '/feed/'
    description = 'Latest Feed Blog Posts'

    def author_name(self):
        return 'Summon Agus'

    def items(self):
        return Post.objects.published_public()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return item.author

    def item_link(self, item):
        return reverse('apps.blog:post_detail', args=[item.slug])

    def item_pubdate(self, item):
        return item.updated_at
