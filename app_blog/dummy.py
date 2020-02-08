import random
from djipsum.faker import FakerModel


def post_faker(maximum=10):
    """
    ./manage.py djipsum -auto -cg=app_blog.dummy.post_faker --max=2
    """
    faker = FakerModel(
        app='app_blog',
        model='Post'
    )
    object_list = []
    for _ in range(maximum):
        fields = {
            'author': faker.fake_relations(type='fk', field_name='author'),
            'title': faker.fake.text(max_nb_chars=100).replace('.', ''),
            'tags': faker.fake_relations(type='m2m', field_name='tags'),
            'description': ' '.join(faker.fake.paragraphs(nb=20)),
            'meta_description': ' '.join(faker.fake.paragraphs()),
            'keywords': faker.fake.text(max_nb_chars=30),
            'is_featured': faker.fake_boolean(),
            'publish': faker.fake_boolean(),
            'created': str(faker.fake.date_time()),
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list


def visitor_faker(maximum=10):
    """
    ./manage.py djipsum -auto -cg=app_blog.dummy.visitor_faker --max=2
    """
    faker = FakerModel(
        app='app_blog',
        model='Visitor'
    )
    object_list = []
    for _ in range(maximum):
        fields = {
            'post': faker.fake_relations(type='fk', field_name='post'),
            'ip': faker.fake.ipv4(),
            'created': str(faker.fake.date_time()),
            'modified': str(faker.fake.date_time()),
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list


def favorite_faker(maximum=10):
    """
    ./manage.py djipsum -auto -cg=app_blog.dummy.favorite_faker --max=2
    """
    faker = FakerModel(
        app='app_blog',
        model='Favorite'
    )
    object_list = []
    for _ in range(maximum):
        fields = {
            'user': faker.fake_relations(type='fk', field_name='user'),
            'post': faker.fake_relations(type='fk', field_name='post'),
            'created': str(faker.fake.date_time()),
            'modified': str(faker.fake.date_time()),
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list
