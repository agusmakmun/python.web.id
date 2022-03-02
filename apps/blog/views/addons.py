"""
Addons Views
to handle all addons models,
like: Visitor, Favorite, Gallery.
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.blog.models.addons import Favorite
from apps.blog.utils.json import JSONResponseMixin


class FavoriteCreateDeleteJSONView(JSONResponseMixin, TemplateView):
    """ Class Bassed View to Create or Delete the Favorite Object """
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
        except ObjectDoesNotExist:
            context_data['message'] = _('This `content_type` doesn\'t exist!')
            return self.render_to_json_response(context_data)

        # get or create the favorite
        queries = {'user': request.user, 'content_type': content_type, 'object_id': object_id}
        favorite, created = self.model.objects.get_or_create(**queries)

        if created or favorite.deleted_at:
            favorite.deleted_at = None
            context_data.update({'success': True, 'message': _('The post marked as favorite!')})
        else:
            favorite.deleted_at = timezone.now()
            context_data.update({'success': True, 'message': _('The post removed from favorite!')})

        favorite.save()

        return self.render_to_json_response(context_data)
