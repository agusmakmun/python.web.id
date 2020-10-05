# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import (Q, Count)
from django.views.generic import (ListView, TemplateView)
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.post import Post
from apps.blog.models.addons import Favorite
from apps.blog.utils.json import JSONResponseMixin


class FavoriteCreateDeleteJSONView(JSONResponseMixin, TemplateView):
    allowed_methods = ('get',)
    model = Favorite

    def get(self, request, *args, **kwargs):
        content_type_name = request.GET.get('content_type')
        object_id = request.GET.get('object_id')
        context_data = {'success': False, 'message': None}

        # validate the request.POST data
        if not all([object_id, content_type_name]):
            context_data['message'] = _('`object_id` and `content_type` must filled!')
            return self.render_to_json_response(context_data)

        if not str(object_id).isdigit():
            context_data['message'] = _('`object_id` should be integer!')
            return self.render_to_json_response(context_data)

        if not request.user.is_authenticated:
            context_data['message'] = _('You must login to mark as favorite!')
            return self.render_to_json_response(context_data)

        try:
            content_type = ContentType.objects.get(model=content_type_name)
        except ContentType.DoesNotExist:
            context_data['message'] = _('This `content_type` doesn\'t exist!')
            return self.render_to_json_response(context_data)

        # get or create the favorite
        queries = {'user': request.user, 'content_type': content_type, 'object_id': object_id}
        favorite, created = self.model.objects.get_or_create(**queries)

        if favorite.deleted_at:
            favorite.deleted_at = None
            context_data.update({'success': True, 'message': _('The post marked as favorite!')})
        else:
            favorite.deleted_at = timezone.now()
            context_data.update({'success': True, 'message': _('The post removed from favorite!')})

        favorite.save()

        return self.render_to_json_response(context_data)
