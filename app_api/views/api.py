# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.db.models import (Q, Count)
from django.utils import timezone
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.parsers import (FormParser, MultiPartParser)
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication, BasicAuthentication
)
from rest_framework.permissions import IsAuthenticated

from app_api.permissions import IsOwnerOrReadOnly
from app_api.serializers import (TagSerializer, PostSerializer,
                                 ProfileSerializer)
from app_blog.utils.paginator import LongRestAPIPagination
from app_blog.models import (Tag, Post, Visitor)
from app_user.models import Profile

# rest authentication usage for development or production mode
REST_AUTHENTICATION = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
if not settings.DEBUG:
    REST_AUTHENTICATION = (TokenAuthentication,)

"""
* SPECIAL LOGIN
    # http://blog.nerdeez.com/?p=377

    curl -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "username={username}&password={password}" \
        http://127.0.0.1:8000/api/v1/login
"""


@api_view(['GET'])
def api_logout(request):
    """
    curl -X GET \
        -H "Authorization: Token {header_token_key}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        http://localhost:8000/api/v1/logout
    """
    auth_token = request.META.get('HTTP_AUTHORIZATION')
    if auth_token == None:
        return Response(data={'detail': _('You are not logged in!')},
                        status=status.HTTP_200_OK)
    else:
        token = auth_token.split('Token ')
        Token.objects.filter(key=token[1]).delete()
        return Response(data={'detail': _('You are logout!')},
                        status=status.HTTP_200_OK)


class AuthView(APIView):
    """
    Check Authentication is needed for this methods

    curl -X GET \
        -H "Authorization: Token {header_token_key}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        http://localhost:8000/api/v1/auth
    """
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {
            'id': request.user.id,
            'username': request.user.username,
            'token': str(request.auth)
        }
        return Response(data)


class TagListView(ListAPIView):
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated,)
    pagination_class = LongRestAPIPagination
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))
        return queryset

    def get(self, request, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          http://localhost:8000/api/v1/tags?q={query}&page={numb}
        """
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        else:
            serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        curl -X POST \
          -H "Authorization: Token {header_token_key}" \
          -d "title={title}&slug={slug}" \
          http://localhost:8000/api/v1/tags
        """
        tags = Tag.objects.filter(title__iexact=request.data['title'])
        if tags.exists():
            return Response({'detail': _('Tag already exist!')},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailView(APIView):
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def get(self, request, slug, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          http://localhost:8000/api/v1/tags/detail/{slug}
        """
        tag = get_object_or_404(Tag, slug=slug)
        serializer = self.serializer_class(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostListView(ListAPIView):
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = PostSerializer

    def get_queryset(self):
        now_year = timezone.now().year
        queryset = Post.objects.published()
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        # only return the queryset filtered by query
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(keywords__icontains=query) | Q(meta_description__icontains=query))

        # sort questions by [newest, featured, views, votes, active]
        if sort == 'featured':
            queryset = queryset.filter(is_featured=True)
        elif sort == 'views':
            top_posts = Visitor.objects.filter(post__in=queryset).values('post')\
                .annotate(total=Count('post__pk')).order_by('-total')
            id_top_posts = [pk['post'] for pk in top_posts]
            filter_posts = list(queryset.filter(pk__in=id_top_posts, modified__year=now_year))
            queryset = sorted(filter_posts, key=lambda i: id_top_posts.index(i.pk))
        elif sort == 'votes':
            queryset = queryset.filter(modified__year=now_year).order_by('-rating_likes')
        elif sort == 'active':
            queryset = queryset.order_by('-modified')
        return queryset

    def get(self, request, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          -H "Content-Type: application/json" \
          -H "Accept: application/json" \
          http://localhost:8000/api/v1/posts?q={query}&
          sort={newest,featured,views,votes,active}&page={numb}
        """
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        else:
            serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        curl -X POST \
          -H "Authorization: Token {header_token_key}" \
          -d "author={username}&title={title}&slug={slug}&
              description={description}&tags={tags}&keywords={keywords}&
              meta_description={meta_description}&publish={publish}" \
          http://localhost:8000/api/v1/posts
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        obj.author = self.request.user


class PostTaggedListView(PostListView):

    def get_object(self, slug):
        return get_object_or_404(Tag, slug=slug)

    def get(self, request, slug, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          http://localhost:8000/api/v1/posts/tagged/{tag_slug}?q={query}&
          sort={newest,featured,views,votes,active}
        """
        tag = self.get_object(slug)
        queryset = self.get_queryset().filter(tags=tag)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostAuthorListView(PostListView):

    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          http://localhost:8000/api/v1/posts/author/{username}?q={query}&
          sort={newest,featured,views,votes,active}
        """
        author = self.get_object(username)
        queryset = self.get_queryset().filter(author=author)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostDetailView(APIView):
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = PostSerializer

    def get_object(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404
        except Post.MultipleObjectsReturned:
            return Post.objects.filter(slug=slug).first()

    def get(self, request, slug, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          http://localhost:8000/api/v1/posts/detail/{slug}
        """
        post = self.get_object(slug)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug, format=None):
        """
        curl -X PUT \
          -H "Authorization: Token {header_token_key}" \
          -d "title={title}&slug={slug}&description={description}&tags={tags}&
              keywords={keywords}&meta_description={meta_description}&publish={publish}" \
          http://localhost:8000/api/v1/posts/detail/{slug}
        """
        post = self.get_object(slug)
        serializer = self.serializer_class(post, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        """
        curl -X DELETE \
          -H "Authorization: Token {header_token_key}" \
          http://localhost:8000/api/v1/posts/detail/{slug}
        """
        post = self.get_object(slug)
        if post.author == request.user:
            post.delete()
            return Response({'detail': _('Post successfully deleted!')},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': _('You are not owner of this post!')},
                        status=status.HTTP_403_FORBIDDEN)


class UserProfileListView(ListAPIView):
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__is_active=True)

    def get(self, request, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          -H "Content-Type: application/json" \
          -H "Accept: application/json" \
          http://localhost:8000/api/v1/users
        """
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        else:
            serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserProfileDetailView(APIView):
    authentication_classes = REST_AUTHENTICATION
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer

    def get_object(self, username):
        return get_object_or_404(Profile, user__username=username)

    def get(self, request, username, format=None):
        """
        curl -X GET \
          -H "Authorization: Token {header_token_key}" \
          -H "Content-Type: application/json" \
          -H "Accept: application/json" \
          http://localhost:8000/api/v1/users/detail/{username}
        """
        profile = self.get_object(username)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        """
        curl -X PUT \
          -H "Authorization: Token {header_token_key}" \
          -d "display_name={display_name}&location={location}&
              about_me={about_me}&website={website}&twitter={twitter}&
              linkedin={linkedin}&github={github}&birth_date={birth_date}" \
          http://localhost:8000/api/v1/users/detail/{username}
        """
        profile = self.get_object(username)
        if profile.user != request.user:
            return Response({'detail': _('You are not owner of this profile!')}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(profile, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
