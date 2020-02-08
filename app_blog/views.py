# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView, UpdateView,
                                  FormView, TemplateView)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models import (Q, Count)

from updown.models import Vote

from app_blog.models import *
from app_blog.forms import (PostForm, TagForm, PageForm, ContactForm)
from app_blog.utils.json import JSONResponseMixin
from app_blog.utils.visitor import visitor_counter
from app_blog.utils.paginator import GenericPaginator
from app_blog.templatetags.post_tags import popular_tags
from app_dashboard.utils.mixins import SuperuserRequiredMixin


class BasePostList(GenericPaginator, ListView):
    paginate_by = settings.PAGINATE_BY
    template_name = 'app_blog/posts_list.html'

    def default_queryset(self):
        """ standard queryset filtered"""
        return Post.objects.published()

    def featured_posts(self):
        """ specific featured posts """
        return self.default_queryset().filter(is_featured=True)

    def additional_context(self):
        """ additional `context_data` for `get_context_data` """
        return None

    def get_queryset(self):
        now_year = timezone.now().year
        queryset = self.default_queryset()
        self.query = self.request.GET.get('q')
        self.sort = self.request.GET.get('sort')

        # only return the queryset filtered by query
        if self.query:
            return queryset.filter(
                Q(title__icontains=self.query) | Q(description__icontains=self.query) |
                Q(keywords__icontains=self.query) | Q(meta_description__icontains=self.query) |
                Q(author__username__icontains=self.query))

        # sort questions by [newest, featured, views, votes, active]
        if self.sort == 'featured':
            queryset = self.featured_posts()
        elif self.sort == 'views':
            top_posts = Visitor.objects.filter(post__in=queryset).values('post')\
                .annotate(total=Count('post__pk')).order_by('-total')
            id_top_posts = [pk['post'] for pk in top_posts]
            filter_posts = list(queryset.filter(pk__in=id_top_posts, modified__year=now_year))
            queryset = sorted(filter_posts, key=lambda i: id_top_posts.index(i.pk))
        elif self.sort == 'favorites':
            top_posts = Favorite.objects.filter(post__in=queryset).values('post')\
                .annotate(total=Count('post__pk')).order_by('-total')
            id_top_posts = [pk['post'] for pk in top_posts]
            filter_posts = list(queryset.filter(pk__in=id_top_posts, modified__year=now_year))
            queryset = sorted(filter_posts, key=lambda i: id_top_posts.index(i.pk))
        elif self.sort == 'votes':
            queryset = queryset.filter(modified__year=now_year).order_by('-rating_likes')
        elif self.sort == 'active':
            queryset = queryset.order_by('-modified')
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super(BasePostList, self).get_context_data(**kwargs)
        context_data['total_posts'] = len(self.get_queryset())
        context_data['total_posts_featured'] = self.featured_posts().count()
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        context_data['sort'] = self.sort
        if self.additional_context():
            context_data.update(**self.additional_context())
        return context_data


class PostList(BasePostList):
    """ extending from default configuration """
    pass


class PostTagged(BasePostList):
    template_name = 'app_blog/posts_tagged.html'

    def default_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags=self.tag).published()

    def additional_context(self):
        return dict(tag=self.tag)


class PostAuthor(BasePostList):
    template_name = 'app_blog/posts_author.html'

    def default_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.author).published()

    def additional_context(self):
        return dict(author=self.author)


class PostAuthorPrivate(LoginRequiredMixin, BasePostList):
    paginate_by = 10
    template_name = 'app_blog/posts_author_private.html'

    def default_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
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


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app_blog/posts_detail.html'

    def post_is_voted(self):
        """
        to check whenever user is voted the post.
        {% if post_is_voted.score == 1 %}orange{% else %}grey{% endif %}
        """
        if self.request.user.is_authenticated:
            votes = Vote.objects.filter(
                content_type__model='post',
                object_id=self.object.id,
                user=self.request.user)
            if votes.exists():
                return votes.first()
        return False

    def related_posts(self, limit):
        return Post.objects.published().filter(
            tags__in=list(self.object.tags.all())
        ).exclude(id=self.object.id).distinct()[:limit]

    def get_context_data(self, **kwargs):
        context_data = super(PostDetail, self).get_context_data(**kwargs)
        context_data['visitor_counter'] = visitor_counter(self.request, self.object)
        context_data['related_posts'] = self.related_posts(5)
        context_data['post_is_voted'] = self.post_is_voted()
        return context_data


class PostCreate(LoginRequiredMixin, FormView):
    template_name = 'app_blog/posts_create.html'
    form_class = PostForm

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.author = self.request.user
        initial.save()
        form.save_m2m()
        messages.success(self.request, _('Post successfully created!'))
        return redirect(reverse('posts_detail', kwargs={'slug': initial.slug}))


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'app_blog/posts_edit.html'
    form_class = PostForm

    def get_object(self):
        """ handle the object for specific permission """
        if self.request.user.is_superuser:
            return get_object_or_404(Post, slug=self.kwargs['slug'])
        return get_object_or_404(Post, slug=self.kwargs['slug'], author=self.request.user)

    def form_valid(self, form):
        post = self.get_object()
        instance = form.save(commit=False)
        instance.author = post.author
        instance.save()
        form.save_m2m()
        messages.success(self.request, _('"%(post)s" successfully updated!') % {'post': instance})
        return redirect(reverse('posts_detail', kwargs={'slug': instance.slug}))

    def get_initial(self):
        initial = super(PostEdit, self).get_initial()
        for field, _cls in self.form_class.base_fields.items():
            if field == 'tags':
                value = self.get_object().tags.all()
            else:
                value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial

    def get_context_data(self, **kwargs):
        context = super(PostEdit, self).get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context


class PostDeleteJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to delete this post!')
            return self.render_to_json_response(context)
        elif request.user.is_superuser:
            post.delete()
            context.update({'success': True, 'message': _('The post deleted!')})
            return self.render_to_json_response(context)
        elif request.user != post.author:
            context['message'] = _('You are not allowed to access this method!')
            return self.render_to_json_response(context)
        else:
            Favorite.objects.filter(post=post).delete()
            Visitor.objects.filter(post=post).delete()
            Vote.objects.filter(content_type__model='post',
                                object_id=post.id).delete()
            post.delete()
            context.update({'success': True, 'message': _('The post deleted!')})
        return self.render_to_json_response(context)


class TagList(GenericPaginator, FormMixin, ListView):
    paginate_by = settings.TAGS_PAGINATE_BY
    form_class = TagForm
    template_name = 'app_blog/tags_list.html'

    def get_queryset(self):
        queryset = popular_tags(limit=self.paginate_by)
        self.query = self.request.GET.get('q')
        if self.query:
            queryset = popular_tags(limit=self.paginate_by, query=self.query)
        return queryset

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You must login to create the tag!'))
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, _('Tag successfully created!'))
            else:
                messages.error(request, _('Tag failed to save!'))
        return redirect('tags_list')

    def get_context_data(self, **kwargs):
        context_data = super(TagList, self).get_context_data(**kwargs)
        context_data['page_range'] = self.get_page_range()
        context_data['query'] = self.query
        return context_data


class TagCreate(LoginRequiredMixin, FormView):
    # not used yet
    template_name = 'app_blog/tags_create.html'
    form_class = TagForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, _('Tag successfully created!'))
        return redirect('tags_list')


class TagCreateJSON(JSONResponseMixin, TemplateView):

    def tag_is_exist(self, tag_name):
        return Tag.objects.filter(slug=tag_name).exists()

    def get(self, request, *args, **kwargs):
        context = {'message': _('request post only!')}
        return self.render_to_json_response(context)

    def post(self, request, *args, **kwargs):
        tag_name = request.POST.get('new-tag')
        context = {'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to create a tag!')
        elif not tag_name or tag_name == '':
            context['message'] = _('Tag should not empty!')
        elif self.tag_is_exist(tag_name):
            context['message'] = _('Tag already exist!')
        else:
            tag = Tag.objects.create(title=tag_name)
            tag.save()
            context['message'] = _('Tag "%(tag)s" successfuly created!') % {'tag': tag}
        return self.render_to_json_response(context)


class TagSearchJSON(JSONResponseMixin, TemplateView):

    def get_queryset(self, query):
        return list(Tag.objects.filter(
            Q(title__startswith=query)).values('title', 'slug', 'id'))

    def get(self, request, *args, **kwargs):
        context = {'success': False, 'results': []}
        query = request.GET.get('q')

        if query is not None and query.strip() != '':
            context.update({'success': True, 'results': self.get_queryset(query)})
        return self.render_to_json_response(context)


class MarkAsFeaturedJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        mode = request.GET.get('mode')
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to mark as featured!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this method!')
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


class FavoriteCrudJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to mark as favorite!')
            return self.render_to_json_response(context)

        favorite = Favorite.objects.filter(user=request.user, post=post)
        if favorite.exists():
            favorite.delete()
            context.update({'success': True, 'message': _('The post removed from favorite!')})
        else:
            Favorite.objects.create(user=request.user, post=post)
            context.update({'success': True, 'message': _('The post marked as favorite!')})
        return self.render_to_json_response(context)


class VoteDeleteJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to undo a vote!')
            return self.render_to_json_response(context)

        status = kwargs['status']
        vote = Vote.objects.filter(content_type__model='post',
                                   object_id=kwargs['post_id'],
                                   user__id=kwargs['user_id'])
        if vote.exists():
            post = vote.first().content_object
            if status == 'likes':
                post.rating.likes -= 1
            else:
                post.rating.dislikes -= 1
            post.save()
            vote.delete()

            context['success'] = True
            context['message'] = _('Undo vote successfully changed!')
        else:
            context['message'] = _("Vote doesn't exists!")
        return self.render_to_json_response(context)


class PageCreate(SuperuserRequiredMixin, FormView):
    template_name = 'app_blog/pages_create.html'
    form_class = PageForm

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.author = self.request.user
        initial.save()
        form.save()
        messages.success(self.request, _('Page successfully created!'))
        return redirect(reverse('pages_detail', kwargs={'slug': initial.slug}))


class PageEdit(SuperuserRequiredMixin, UpdateView):
    template_name = 'app_blog/pages_edit.html'
    form_class = PageForm

    def get_object(self):
        return get_object_or_404(Page, slug=self.kwargs['slug'])

    def form_valid(self, form):
        page = self.get_object()
        instance = form.save(commit=False)
        instance.author = page.author
        instance.save()
        form.save()
        messages.success(self.request, _('"%(page)s" successfully updated!') % {'page': instance})
        return redirect(reverse('pages_detail', kwargs={'slug': instance.slug}))

    def get_initial(self):
        initial = super(PageEdit, self).get_initial()
        for field, _cls in self.form_class.base_fields.items():
            value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial


class PageDetail(DetailView):
    model = Page
    context_object_name = 'page'
    template_name = 'app_blog/pages_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super(PageDetail, self).get_context_data(**kwargs)
        context_data['site_pages'] = Page.objects.filter(status='site').published()
        return context_data


class PageDeleteJSON(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        page = get_object_or_404(Page, pk=kwargs['pk'])
        context = {'success': False, 'message': None}

        if not request.user.is_authenticated:
            context['message'] = _('You must login to delete this page!')
            return self.render_to_json_response(context)
        elif not request.user.is_superuser:
            context['message'] = _('You are not allowed to access this method!')
            return self.render_to_json_response(context)
        else:
            page.delete()
            context.update({'success': True, 'message': _('The page deleted!')})
        return self.render_to_json_response(context)


class ContactUs(FormView):
    template_name = 'app_blog/contact_us.html'
    form_class = ContactForm

    def get_form_kwargs(self):
        kwargs = super(ContactUs, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        sender = form.cleaned_data['sender']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['email']

        subject = '%s from %s:%s' % (subject, sender, from_email)
        recipients = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, recipients)

        messages.success(self.request, _('Your message successfully sended!'))
        return redirect('posts_list')
