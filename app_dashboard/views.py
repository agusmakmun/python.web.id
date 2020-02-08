# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.db.models import (Q, Count)
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView, FormView,
                                  UpdateView, TemplateView)
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User

from app_blog.forms import TagForm
from app_blog.views import (BasePostList)
from app_blog.models import (Post, Tag, Page, Visitor, Gallery)
from app_blog.utils.paginator import GenericPaginator
from app_blog.utils.json import JSONResponseMixin
from app_dashboard.utils.mixins import SuperuserRequiredMixin
from app_dashboard.forms import GalleryForm


class DashboardHome(SuperuserRequiredMixin, TemplateView):
    template_name = 'app_dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context_data = super(DashboardHome, self).get_context_data(**kwargs)
        context_data['total_tags'] = Tag.objects.all().count()
        context_data['total_posts'] = Post.objects.all().count()
        context_data['total_users'] = User.objects.all().count()
        context_data['total_galleries'] = Gallery.objects.all().count()
        context_data['total_visitors'] = Visitor.objects.all().count()
        return context_data


class DashboardPosts(SuperuserRequiredMixin, BasePostList):
    template_name = 'app_dashboard/dashboard_posts.html'
    #paginate_by = settings.PAGINATE_BY
    paginate_by = 20

    def default_queryset(self):
        queryset = Post.objects.order_by('-created')
        self.is_published = self.request.GET.get('is_published')
        self.is_featured = self.request.GET.get('is_featured')

        if self.is_published == 'yes':
            queryset = queryset.published()
        elif self.is_published == 'no':
            queryset = queryset.unpublished()

        if self.is_featured == 'yes':
            queryset = queryset.filter(is_featured=True)
        elif self.is_featured == 'no':
            queryset = queryset.filter(is_featured=False)

        return queryset

    def additional_context(self):
        return dict(is_published=self.is_published,
                    is_featured=self.is_featured)


class DashboardTags(SuperuserRequiredMixin, GenericPaginator, FormMixin, ListView):
    template_name = 'app_dashboard/dashboard_tags.html'
    form_class = TagForm
    paginate_by = 20

    def get_queryset(self):
        queryset = Tag.objects.order_by('-created')
        self.query = self.request.GET.get('q')
        if self.query:
            queryset = queryset.filter(Q(title__icontains=self.query))
        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # delete mode via ajax response
            if request.POST.get('delete'):
                tag_id = request.POST.get('tag_delete_id')
                tag = get_object_or_404(Tag, pk=tag_id)
                tag.delete()
                messages.success(request, _('Tag successfully deleted!'))
                return redirect('dashboard_tags')

            # create and edit mode via form
            tag_id = request.POST.get('tag_id')
            if tag_id:
                tag = get_object_or_404(Tag, pk=tag_id)
                form = self.form_class(request.POST, instance=tag)
            else:
                form = self.form_class(request.POST)
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, _('Tag successfully created!'))
            else:
                messages.error(request, _('Tag failed to save!'))
        else:
            messages.error(request, _('You must login to create the tag!'))
        return redirect('dashboard_tags')

    def get_context_data(self, **kwargs):
        context_data = super(DashboardTags, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        return context_data


class DashboardPages(SuperuserRequiredMixin, GenericPaginator, ListView):
    template_name = 'app_dashboard/dashboard_pages.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Page.objects.order_by('-created')
        self.query = self.request.GET.get('q')
        if self.query:
            queryset = queryset.filter(Q(title__icontains=self.query))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super(DashboardPages, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        return context_data


class DashboardGalleries(SuperuserRequiredMixin, GenericPaginator, ListView):
    template_name = 'app_dashboard/dashboard_galleries.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Gallery.objects.order_by('-created')
        self.query = self.request.GET.get('q')
        if self.query:
            queryset = queryset.filter(Q(title__icontains=self.query) |
                                       Q(attachment__icontains=self.query) |
                                       Q(author__username__icontains=self.query))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super(DashboardGalleries, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        return context_data


class DashboardGalleryCreate(SuperuserRequiredMixin, FormView):
    template_name = 'app_dashboard/dashboard_galleries_create.html'
    form_class = GalleryForm

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.author = self.request.user
        initial.save()
        form.save()
        messages.success(self.request, _('File successfully uploaded!'))
        return redirect('dashboard_galleries')


class DashboardGalleryEdit(SuperuserRequiredMixin, UpdateView):
    template_name = 'app_dashboard/dashboard_galleries_edit.html'
    form_class = GalleryForm

    def get_object(self):
        return get_object_or_404(Gallery, pk=self.kwargs['pk'])

    def form_valid(self, form):
        gallery = self.get_object()
        instance = form.save(commit=False)
        instance.author = gallery.author
        instance.save()
        form.save()
        messages.success(self.request, _('"%(file)s" successfully updated!') % {'file': instance})
        return redirect('dashboard_galleries')

    def get_initial(self):
        initial = super(DashboardGalleryEdit, self).get_initial()
        for field, _cls in self.form_class.base_fields.items():
            value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial

    def get_context_data(self, **kwargs):
        context = super(DashboardGalleryEdit, self).get_context_data(**kwargs)
        context['gallery'] = self.get_object()
        return context


class DashboardGalleryDeleteJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        gallery = get_object_or_404(Gallery, pk=kwargs['pk'])
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to delete this file!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this method!')
            return self.render_to_json_response(context)
        else:
            import os
            file_path = gallery.attachment.path
            if os.path.exists(file_path):
                os.remove(file_path)

            gallery.delete()
            context.update({'success': True, 'message': _('The file deleted!')})
        return self.render_to_json_response(context)


class DashboardVisitors(SuperuserRequiredMixin, GenericPaginator, ListView):
    template_name = 'app_dashboard/dashboard_visitors.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Visitor.objects.order_by('-created')
        self.query = self.request.GET.get('q')
        if self.query:
            queryset = queryset.filter(Q(post__title__icontains=self.query) |
                                       Q(ip__icontains=self.query))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super(DashboardVisitors, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        return context_data


class DashboardVisitorDeleteJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        visitor = get_object_or_404(Visitor, pk=kwargs['pk'])
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to delete this visitor!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this method!')
            return self.render_to_json_response(context)
        else:
            visitor.delete()
            context.update({'success': True, 'message': _('The visitor deleted!')})
        return self.render_to_json_response(context)


class DashboardUsers(SuperuserRequiredMixin, GenericPaginator, ListView):
    template_name = 'app_dashboard/dashboard_users.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.order_by('-date_joined')
        self.query = self.request.GET.get('q')
        if self.query:
            queryset = queryset.filter(Q(username__icontains=self.query) |
                                       Q(email__icontains=self.query))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super(DashboardUsers, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        return context_data


class DashboardUserActivationJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        mode = request.GET.get('mode', 'deactivate')
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to delete this user!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this method!')
            return self.render_to_json_response(context)
        else:
            if mode == 'deactivate':
                user.is_active = False
                user.save()
                context.update({'success': True, 'message': _('User successfully unactivated!')})
            else:
                user.is_active = True
                user.save()
                context.update({'success': True, 'message': _('User successfully activated!')})
        return self.render_to_json_response(context)


class DashboardUserDeleteJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to delete this user!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this method!')
            return self.render_to_json_response(context)
        else:
            user.delete()
            context.update({'success': True, 'message': _('The user deleted!')})
        return self.render_to_json_response(context)
