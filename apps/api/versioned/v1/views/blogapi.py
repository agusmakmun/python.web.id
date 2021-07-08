import requests

from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model

from apps.blog.models.tag import Tag
from apps.blog.models.post import Post

User = get_user_model()


class PythonWebIdAPI(object):

    def __init__(self, username, password):
        self.base_url = 'https://python.web.id'
        self.token = None
        self.headers = None
        self.username = username
        self.password = password
        self.setup_token_login(self.username, self.password)

    def setup_token_login(self, username: str, password: str):
        url = f'{self.base_url}/api/v1/auth/login/'
        request_data = {'username': username, 'password': password}
        response = requests.post(url, data=request_data)
        response_json = response.json()
        if response_json.get('success'):
            self.token = response_json.get('result', {}).get('token')
            self.headers = {'Authorization': f'Token {self.token}'}
        return self.token, self.headers

    def get_posts_ids(self):
        if not self.headers:
            raise Exception('Headers is required.')

        posts_ids = []
        url = f'{self.base_url}/api/v1/post/'
        response = requests.get(url, headers=self.headers)
        response_json = response.json()

        page_size = response_json.get('page_size', 0)
        current_page = 0
        while current_page <= page_size:
            current_page += 1
            url = f'{url}?page={current_page}'
            response = requests.get(url, headers=self.headers)
            response_json = response.json()

            for post_data in response_json.get('results', []):
                post_id = post_data.get('id')
                if isinstance(post_id, int) and (post_id not in posts_ids):
                    posts_ids.append(post_id)

        # sort ids by oldest creation
        posts_ids = sorted(posts_ids)
        return posts_ids

    def sync_posts(self):
        print('[i] Retrieving all posts ids, please wait...')
        posts_ids = self.get_posts_ids()
        print('[i] All ids successfully retrieved.')
        print('[i] Synchronizing the posts, please wait...')

        for post_id in posts_ids:
            url = f'{self.base_url}/api/v1/post/?id={post_id}'
            response = requests.get(url, headers=self.headers)
            response_json = response.json()

            if response_json.get('success'):
                result = response_json.get('result', {})
                post_slug = result.get('slug')

                author_username = result.get('author')
                author = User.objects.filter(username=author_username).first()
                if not author:
                    author = User.objects.create_user(
                        username=author_username,
                        password=self.password
                    )

                post, __ = Post.objects.update_or_create(
                    slug=post_slug,
                    defaults={
                        'author': author,
                        'title': result.get('title'),
                        'description': result.get('description'),
                        'created_at': parse_datetime(result.get('created_at')),
                        'updated_at': parse_datetime(result.get('updated_at')),
                        'keywords': result.get('keywords'),
                        'meta_description': result.get('meta_description'),
                        'is_featured': result.get('is_featured')
                    }
                )

                tags = []
                for tag_data in result.get('tags', []):
                    tag = Tag.objects.update_or_create(
                        name=tag_data.get('name'),
                        defaults={'description': tag_data.get('description')}
                    )[0]
                    tags.append(tag)

                post.tags.set(tags)
                post.save()

                print('[i] Post %s successfully created.' % post)
