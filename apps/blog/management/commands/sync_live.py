# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from apps.api.versioned.v1.views.blogapi import PythonWebIdAPI


class Command(BaseCommand):
    help = 'Sync local data from server live.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str)
        parser.add_argument('--password', type=str)

    def handle(self, *args, **options):
        username = options.get('username')
        password = options.get('password')

        if not all([username, password]):
            print('[!] Username & Password is required.')
            return self.print_help('sync_live', '-h')

        api = PythonWebIdAPI(username, password)
        api.sync_posts()
