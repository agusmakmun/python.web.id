# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import transaction

from stackapi import StackAPI, StackAPIError
from html2markdown import convert as convert_to_markdown
from apps.blog.models.post import Post
from apps.blog.models.tag import Tag

logger = logging.getLogger('StackOverFlowAPI')
User = get_user_model()


class StackOverFlowAPI:

    def __init__(self, *args, **kwargs):
        # StackAPI
        self.tagged = kwargs.get('tagged', 'django')
        self.pagesize = kwargs.get('pagesize', 30)
        self.page = kwargs.get('page', 1)
        self.sort = kwargs.get('sort', 'votes')
        self.todate = kwargs.get('todate', timezone.now())
        self.fromdate = kwargs.get(
            'fromdate', self.todate - timezone.timedelta(days=30 * 6)
        )

        # Django Object
        self.max_objects = kwargs.get('max_objects', 1)
        self.author = kwargs.get(
            'author', User.objects.filter(is_superuser=True).first()
        )
        super().__init__(*args, **kwargs)

    def run(self):
        """ https://stackoverflow.com/a/53751903/6396981 """
        try:
            logger.info(f'GET the {self.tagged} questions')
            SITE = StackAPI('stackoverflow')
            response_json = SITE.fetch(
                'questions',
                tagged=self.tagged,
                pagesize=self.pagesize,
                page=self.page,
                sort=self.sort,
                fromdate=self.fromdate,
                todate=self.todate,
                filter=('!)P9f6C0TNwV_moNthNdldw-WtbW2HacuOCk)'
                        'rnIGL5j1KEVT.4t51tU7I-eV1B0VJnD4dD')
            )
            logger.info('Create the questions to objects...')
            self.create_objects(response_json)
        except StackAPIError as error:
            logger.error(str(error))

    @transaction.atomic
    def create_objects(self, response_json):
        for item_data in response_json.get('items', []):
            # stop the process
            if self.max_objects < 1:
                break

            # makesure the question already answered,
            # and the question is not downvoted.
            if item_data.get('is_answered') and item_data.get('score', 0) > 10:
                post_data = {
                    'author': self.author,
                    'title': item_data.get('title'),
                    'slug': slugify(item_data.get('title')),
                    'description': self.get_description(item_data),
                    'keywords': None,
                    'meta_description': None,
                    'is_featured': False,
                    'publish': True
                }
                if not Post.objects.filter(slug=post_data['slug']).exists():
                    post = Post.objects.create(**post_data)
                    post.tags.add(*self.get_tags(item_data.get('tags', [])))
                    post.save()
                    logger.info(f'Object {post} is created.')
                    self.max_objects -= 1

    def get_description(self, item_data):
        question = convert_to_markdown(item_data.get('body'))
        answer = self.get_accepted_answer(item_data)
        link = item_data.get('link')
        return (
            f'{question} \n\n'
            f'### Answer\n\n{answer} \n\n'
            f'**Source:** {link}'
        )

    def get_accepted_answer(self, item_data):
        for answer_data in item_data.get('answers', []):
            if answer_data['is_accepted']:
                return convert_to_markdown(answer_data.get('body'))
        return '-'

    def get_tags(self, list_tags):
        tags = []
        for tag_name in list_tags:
            try:
                tags.append(
                    Tag.objects.get_or_create(
                        name=slugify(tag_name)
                    )[0]
                )
            except Tag.MultipleObjectsReturned:
                pass  # skip swaped data
        return tags
