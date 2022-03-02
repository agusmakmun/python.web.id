"""
Post Views
to handle all post models,
like: Post, Tag
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import strip_tags
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView, UpdateView,
                                  FormView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.blog.models.tag import Tag
from apps.blog.models.post import Post
from apps.blog.models.addons import (Visitor, Favorite)
from apps.blog.utils.visitor import (visitor_counter, get_popular_objects)
from apps.blog.utils.json import JSONResponseMixin
from apps.blog.forms.post import PostForm
from apps.accounts.models.user import User
from apps.blog.templatetags.common_tags import markdown_find_images
from martor.templatetags.martortags import safe_markdown


class PostListView(ListView):
    """ Class View to show the Posts """
    paginate_by = getattr(settings, 'DEFAULT_PAGINATION_NUMBER', 10)
    template_name = 'apps/blog/post/list.html'
    queryset = Post.objects.published_public()
    context_object_name = 'posts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = None
        self.sort = None

    def get_default_queryset(self):
        """ need this to implement overwrite the default queryset """
        return self.queryset

    def featured_posts(self):
        """ specific featured posts """
        return self.get_default_queryset().filter(is_featured=True)

    def get_queryset(self):
        queryset = self.get_default_queryset()\
                       .select_related('author')\
                       .prefetch_related('tags')
        self.query = self.request.GET.get('q')
        self.sort = self.request.GET.get('sort', 'newest')

        if self.query:
            queryset = queryset.filter(
                Q(title__iexact=self.query) | Q(title__icontains=self.query) |
                Q(description__iexact=self.query) | Q(description__icontains=self.query) |
                Q(keywords__iexact=self.query) | Q(keywords__icontains=self.query)
            )

        if self.sort == 'featured':
            queryset = queryset.filter(is_featured=True)
        elif self.sort == 'views':
            # this queryset below will return as list objects, e.g:
            # [<Post: NMD R1 Black and Blue Shoes>, <Post: Lorem ipsum>, ...]
            # so, the `total_posts` should not handled with `.count()` method.
            queryset = get_popular_objects(queryset=queryset, addon_model=Visitor)
        elif self.sort == 'favorites':
            # this queryset below will return as list objects, e.g:
            # [<Post: NMD R1 Black and Blue Shoes>, <Post: Lorem ipsum>, ...]
            # so, the `total_posts` should not handled with `.count()` method.
            queryset = get_popular_objects(queryset=queryset, addon_model=Favorite)
        elif self.sort == 'votes':
            queryset = queryset.order_by('-rating_likes')
        elif self.sort == 'active':
            queryset = queryset.order_by('-updated_at')

        return queryset

    @property
    def extra_context(self):
        """ additional `context_data` for `get_context_data` """
        return None

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total_posts'] = len(self.get_queryset())
        context_data['total_posts_featured'] = self.featured_posts().count()
        context_data['query'] = self.query
        if self.extra_context:
            context_data.update(**self.extra_context)
        return context_data


class PostListTaggedView(PostListView):
    """ Class View to filter Posts by specific Tag """
    template_name = 'apps/blog/post/tagged.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = None

    def get_default_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['name'])
        return self.tag.post_set.published_public()

    @property
    def extra_context(self):
        return dict(tag=self.tag)


class PostListAuthorView(PostListView):
    """ Class View to filter Posts by specific author """
    template_name = 'apps/blog/post/author.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = None

    def get_default_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return self.author.post_set.published_public()

    @property
    def extra_context(self):
        return dict(author=self.author)


class PostListAuthorPrivateView(LoginRequiredMixin, PostListView):
    """ Class View to filter Posts by specific author (his own posts) """
    template_name = 'apps/blog/post/list_private.html'
    queryset = Post.objects.published()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publish = None
        self.is_featured = None

    def get_default_queryset(self):
        queryset = self.queryset.filter(author=self.request.user)
        self.publish = self.request.GET.get('publish')
        self.is_featured = self.request.GET.get('is_featured')

        if self.publish == 'yes':
            queryset = queryset.filter(publish=True)
        elif self.publish == 'no':
            queryset = queryset.filter(publish=False)

        if self.is_featured == 'yes':
            queryset = queryset.filter(is_featured=True)
        elif self.is_featured == 'no':
            queryset = queryset.filter(is_featured=False)

        return queryset

    @property
    def extra_context(self):
        return dict(publish=self.publish,
                    is_featured=self.is_featured)


class PostDetailView(DetailView):
    """ Class View to show detail of Post object """
    template_name = 'apps/blog/post/detail.html'
    context_object_name = 'post'
    model = Post

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, slug=self.kwargs['slug'],
                                 deleted_at__isnull=True)

    def get_related_posts(self, limit=5):
        """
        function to get the related posts.
        :param `limit` is integer limit of total posts.
        :return posts object
        """
        queries = {'tags__in': self.object.tags.all()}
        return self.model.objects.published_public()\
                                 .filter(**queries)\
                                 .exclude(id=self.object.id)\
                                 .distinct()[:limit]

    @property
    def user_post_vote(self):
        """
        to check whenever user is voted the post.
        {% if user_post_vote %}orange{% else %}grey{% endif %}
        """
        if self.request.user.is_authenticated:
            return self.object.rating.get_rating_for_user(user=self.request.user)
        return False

    def get_visitors(self):
        """
        function to get/create the visitor,
        :return dict of {'client_ip': <str>, 'total_visitors': <int>}
        """
        queries = {'request': self.request,
                   'content_type': self.object.get_content_type(),
                   'object_id': self.object.id}
        return visitor_counter(**queries)

    def get_meta_description(self):
        if self.object.meta_description:
            return self.object.meta_description
        return Truncator(
            strip_tags(safe_markdown(self.object.description))
        ).words(20)

    def get_image_urls(self):
        return markdown_find_images(self.object.description)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['related_posts'] = self.get_related_posts(limit=5)
        context_data['user_post_vote'] = self.user_post_vote
        context_data['visitor_counter'] = self.get_visitors()
        context_data['meta_description'] = self.get_meta_description()
        context_data['image_urls'] = self.get_image_urls()
        return context_data


class PostCreateView(LoginRequiredMixin, FormView):
    """ Class View to create the Post object """
    template_name = 'apps/blog/post/create.html'
    form_class = PostForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        form.save_m2m()
        messages.success(self.request, _('Post successfully created!'))
        return redirect(reverse('apps.blog:post_detail', kwargs={'slug': instance.slug}))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """ Class View to update the Post object """
    template_name = 'apps/blog/post/update.html'
    context_object_name = 'post'
    form_class = PostForm
    model = Post

    def get_object(self, queryset=None):
        """ handle the object for specific permission """
        if self.request.user.is_superuser:
            return get_object_or_404(self.model, slug=self.kwargs['slug'])
        return get_object_or_404(self.model, slug=self.kwargs['slug'], author=self.request.user)

    def form_valid(self, form):
        post = self.get_object()
        instance = form.save(commit=False)
        instance.author = post.author
        instance.save()
        form.save_m2m()
        messages.success(self.request, _('"%(post)s" successfully updated!') % {'post': instance})
        return redirect(reverse('apps.blog:post_detail', kwargs={'slug': instance.slug}))

    def get_initial(self):
        initial = super().get_initial()
        for field, _cls in self.form_class.base_fields.items():
            if field == 'tags':
                value = self.get_object().tags.all()
            else:
                value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post'] = self.get_object()
        return context


class PostDeleteJSONView(JSONResponseMixin, TemplateView):
    """ Class View to delete the Post object via json format """
    model = Post

    def soft_delete_post(self, post):
        """
        function to delete the post object with soft delete method
        :param `post` is object of `Post`.
        :return
        """
        # soft delete the related objects
        queries = {'content_type__model': 'post', 'object_id': post.id}
        Visitor.objects.filter(**queries).update(deleted_at=timezone.now())
        Favorite.objects.filter(**queries).update(deleted_at=timezone.now())

        # soft delete the object
        post.deleted_at = timezone.now()
        post.save()

    def get(self, request, *args, **kwargs):
        context_data = {'success': False, 'message': None}
        object_id = request.GET.get('id')

        if str(object_id).isdigit():
            post = get_object_or_404(self.model, id=object_id)

            if not request.user.is_authenticated:
                context_data['message'] = _('You must login to delete this post!')
            elif request.user.is_superuser:
                self.soft_delete_post(post=post)
                context_data['success'] = True
                context_data['message'] = _('The successfully post deleted!')
            elif request.user != post.author:
                context_data['message'] = _('You are not allowed to access this feature!')
            else:
                self.soft_delete_post(post=post)
                context_data['success'] = True
                context_data['message'] = _('The successfully post deleted!')
        else:
            context_data['message'] = _('Param `id` should be integer!')

        return self.render_to_json_response(context_data)


class PostMarkAsFeaturedJSONView(JSONResponseMixin, TemplateView):
    """ Class view to mark a post as featured post """
    model = Post

    def get(self, request, *args, **kwargs):
        mode = request.GET.get('mode')
        context = {'success': False, 'message': None}
        post = get_object_or_404(self.model, id=kwargs['id'])

        if not request.user.is_authenticated:
            context['message'] = _('You must login to mark as featured!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this feature!')
            return self.render_to_json_response(context)
        else:
            if mode == 'yes':
                post.is_featured = True
                context.update({'message': _('The post marked as featured!')})
            else:
                post.is_featured = False
                context.update({'message': _('The post removed from featured!')})
            post.save()
            context.update({'success': True})
        return self.render_to_json_response(context)
