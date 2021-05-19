# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (Q, Count)
from django.views.generic import (ListView, TemplateView)
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.tag import Tag
from apps.blog.utils.json import JSONResponseMixin


class TagListView(ListView):
    template_name = 'apps/blog/tag/list.html'
    queryset = Tag.objects.published()
    context_object_name = 'tags'
    paginate_by = 16

    def get_queryset(self):
        queryset = self.queryset
        self.sort = self.request.GET.get('sort', 'popular')
        self.query = self.request.GET.get('q')

        if self.query:
            queryset = queryset.filter(name__icontains=self.query)
        if self.sort == 'name':
            return queryset.order_by('name')
        elif self.sort == 'new':
            return queryset.order_by('-created_at')
        return queryset.annotate(total=Count('post')).order_by('-total')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['query'] = self.query
        context_data['sort'] = self.sort
        return context_data


class TagJSONSearchView(JSONResponseMixin, TemplateView):
    model = Tag

    def get_queryset(self, query):
        return list(
            self.model.objects.filter(Q(name__startswith=query))
            .values('name', 'id')
        )

    def get(self, request, *args, **kwargs):
        context_data = {'success': False, 'results': []}
        query = request.GET.get('q', '')
        if query != '':
            context_data.update({'success': True, 'results': self.get_queryset(query)})
        return self.render_to_json_response(context_data)


class TagJSONCreateView(JSONResponseMixin, TemplateView):
    allowed_methods = ('post',)
    model = Tag

    def post(self, request, *args, **kwargs):
        context_data = {'message': None}
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not request.user.is_authenticated:
            context_data['message'] = _('You must login to create a tag!')
        elif not name:
            context_data['message'] = _('Tag should not empty!')
        elif self.model.objects.filter(name=name).exists():
            context_data['message'] = _('Tag already exist!')
        else:
            queries = {'name': name, 'description': description}
            tag = self.model.objects.create(**queries)
            context_data['message'] = _('Tag "%(tag)s" successfuly created!') % {'tag': tag}

        return self.render_to_json_response(context_data)

    # def get(self, request, *args, **kwargs):
    #     context = {'message': _('request post only!')}
    #     return self.render_to_json_response(context)
