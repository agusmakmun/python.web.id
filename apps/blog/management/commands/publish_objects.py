# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.core.management.base import BaseCommand
from apps.blog.models.post import Post


class Command(BaseCommand):
    help = ('Command to publish the drafted objects.')

    def add_arguments(self, parser):
        parser.add_argument('--max_objects', type=int, default=1)

    def handle(self, *args, **options):
        max_objects = options.get('max_objects')
        posts = Post.objects.filter(
            publish=False,
            deleted_at__isnull=True
        )[:max_objects]
        for post in posts:
            post.created_at = timezone.now()
            post.publish = True
            post.save()
