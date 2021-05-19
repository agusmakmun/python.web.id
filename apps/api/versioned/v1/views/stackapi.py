# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import html
import logging

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import transaction

from stackapi import StackAPI, StackAPIError
from apps.blog.models.post import Post
from apps.blog.models.tag import Tag

logger = logging.getLogger('StackOverFlowAPI')
User = get_user_model()


class StackOverFlowAPI:

    def __init__(self, *args, **kwargs):
        # StackAPI
        self.tagged = kwargs.get('tagged')
        self.pagesize = kwargs.get('pagesize', 30)
        self.page = kwargs.get('page', 1)
        self.sort = kwargs.get('sort', 'hot')
        self.todate = kwargs.get('todate', timezone.now())
        self.fromdate = kwargs.get(
            'fromdate', self.todate - timezone.timedelta(days=7)
        )

        # Django Object
        self.publish = kwargs.get('publish', False)
        self.max_objects = kwargs.get('max_objects', self.pagesize)
        self.author = kwargs.get(
            'author', User.objects.filter(is_superuser=True).first()
        )
        super().__init__(*args, **kwargs)

    def run(self):
        """
        https://stackoverflow.com/a/53751903/6396981
        https://api.stackexchange.com/docs/questions
        """
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
                filter=('!GjCqwCMIq7tZmaZn3681-ucQupkeQ1iziaUSmCpPx3-'
                        'uXCx_YEstRpaae0AlFdI(BAk-s5sGfb.iyfRY19')
            )
            logger.info('Create the questions to objects...')
            self.create_objects(response_json)
        except StackAPIError as error:
            logger.error(str(error))

    @transaction.atomic
    def create_objects(self, response_json):
        """
        function to create Question, Answer, and Tag objects.
        :param `response_json` is response.json()
        :return
        """
        for item_data in response_json.get('items', []):
            # stop the process
            if self.max_objects < 1:
                break

            # makesure the question already answered,
            # and the question is not downvoted.
            if item_data.get('is_answered') and item_data.get('score', 0) >= 1:
                post_data = {
                    'author': self.author,
                    'title': html.unescape(item_data.get('title')),
                    'description': self.get_description(item_data),
                    'keywords': None,
                    'meta_description': None,
                    'is_featured': False,
                    'publish': self.publish
                }
                slug = slugify(post_data['title'])[:200]

                # Create/Update a Question Object
                post = Post.objects.update_or_create(
                    slug=slug,
                    defaults=post_data
                )[0]
                post.tags.set(self.get_or_create_tags(
                    item_data.get('tags', []))
                )
                post.save()

                logger.info(f'Object {post} is created.')
                self.max_objects -= 1

    def get_description(self, item_data):
        question = html.unescape(item_data.get('body_markdown'))
        answer = self.get_answer(item_data)
        link = item_data.get('share_link')
        return (
            f'{question} \n\n'
            f'### Answer\n\n{answer} \n\n'
            f'**Source:** {link}'
        )

    def get_answer(self, item_data):
        list_answers_data = item_data.get('answers', [])
        accepted_answer_data = {}

        for answer_data in list_answers_data:
            if answer_data['is_accepted']:
                accepted_answer_data = answer_data
                break

        # we will prior accepted_answer_data
        if accepted_answer_data:
            return html.unescape(accepted_answer_data.get('body_markdown'))

        # if accepted_answer_data not found, then
        # we will use the largest score.
        list_answers_data = sorted(list_answers_data, key=lambda k: k['score'])
        if len(list_answers_data) > 0:
            top_answer_data = list_answers_data[0]
            return html.unescape(top_answer_data.get('body_markdown'))
        return ''

    def get_or_create_tags(self, list_tags):
        """
        function to get or create the tag objects.
        :param `list_tags` is list string of tags.
        :return list Tag objects
        """
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
