# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from apps.api.versioned.v1.views.stackapi import StackOverFlowAPI


class Command(BaseCommand):
    help = ('Scrap questions data from StackOverFlow, '
            'then create it as Post objects.')

    def add_arguments(self, parser):
        parser.add_argument('--tagged', type=str, default='django')
        parser.add_argument('--pagesize', type=int, default=30)
        parser.add_argument('--page', type=int, default=1)
        parser.add_argument('--sort', type=str, default='votes')
        parser.add_argument('--max_objects', type=int, default=1)

    def handle(self, *args, **options):
        api = StackOverFlowAPI()
        api.tagged = options.get('tagged')
        api.pagesize = options.get('pagesize')
        api.page = options.get('page')
        api.sort = options.get('sort')
        api.max_objects = options.get('max_objects')
        api.run()
