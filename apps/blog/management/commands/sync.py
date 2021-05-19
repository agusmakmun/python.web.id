# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from apps.blog.models.tag import Tag
from apps.blog.models.post import Post
from apps.blog.models.addons import Visitor
from apps.accounts.models.user import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Sync & generate an existing data.'
    base_path = os.path.join(settings.BASE_DIR, '.ext/dummies')

    def sync_users(self):
        """ function to sync the existing users """
        path = os.path.join(self.base_path, 'users.json')

        if os.path.exists(path):
            user_data = json.load(open(path))
            user_data.reverse()

            for item in user_data:
                try:
                    user = User(**item)
                    user.save()
                except Exception:
                    pass

    def sync_profiles(self):
        """ function to sync the existing profiles """
        path = os.path.join(self.base_path, 'profiles.json')

        if os.path.exists(path):
            profile_data = json.load(open(path))
            profile_data.reverse()

            for item in profile_data:
                user = User.objects.get(username=item.get('user__username'))
                item['user'] = user
                item['birth_date'] = item.get('birth_date_at')

                del item['user__username']
                del item['birth_date_at']

                try:
                    user = Profile(**item)
                    user.save()
                except Exception:
                    pass

    def sync_tags(self):
        """ function to sync the existing tags """
        path = os.path.join(self.base_path, 'tags.json')

        if os.path.exists(path):
            tag_data = json.load(open(path))
            tag_data.reverse()

            for tag_slug in tag_data:
                Tag.objects.get_or_create(name=tag_slug)

    def sync_posts(self):
        """ function to sync the existing posts """
        path = os.path.join(self.base_path, 'posts.json')

        if os.path.exists(path):
            post_data = json.load(open(path))
            post_data.reverse()

            for item in post_data:
                author = User.objects.get(username=item.get('author'))
                created_at = item.get('created_at')
                updated_at = item.get('updated_at')

                item['author'] = author
                item['created_at'] = created_at[:10] + ' ' + created_at[11:19]
                item['updated_at'] = updated_at[:10] + ' ' + updated_at[11:19]

                tags = item.get('tags', [])
                tags = Tag.objects.filter(name__in=tags)

                del item['tags']
                del item['rating_likes']
                del item['rating_dislikes']
                del item['total_visitors']
                del item['total_favorites']

                try:
                    post, _ = Post.objects.get_or_create(**item)
                    post.tags.add(*tags)
                    post.save()
                except Exception:
                    pass

    def sync_visitors(self):
        """ function to sync the existing visitors """
        path = os.path.join(self.base_path, 'visitors.json')

        if os.path.exists(path):
            visitor_data = json.load(open(path))
            visitor_data.reverse()

            for item in visitor_data:
                try:
                    post = Post.objects.get(slug=item.get('post__slug'))
                    content_type = ContentType.objects.get_for_model(post)
                    item_new = {
                        'ip_address': item.get('ip'),
                        'object_id': post.id,
                        'content_type': content_type
                    }
                    visitor = Visitor(**item_new)
                    visitor.save()
                except Exception:
                    pass

    def handle(self, *args, **options):
        self.sync_users()
        self.sync_profiles()
        self.sync_tags()
        self.sync_posts()
        self.sync_visitors()
