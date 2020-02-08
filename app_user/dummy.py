import random
from djipsum.faker import FakerModel
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def check_username(username):
    numb = 1
    username = username
    while User.objects.filter(username=username).exists():
        username = '%s-%d' % (username, numb)
        numb += 1
    return username


def user_faker(maximum=10):
    """
    ./manage.py djipsum -auto -cg=app_user.dummy.user_faker --max=2
    """
    faker = FakerModel(
        app='auth',
        model='User'
    )
    object_list = []
    for _ in range(maximum):
        fields = {
            'username': check_username(faker.fake.profile(fields=['username'])['username']),
            'password': make_password('Informatika113'),
            'first_name': faker.fake.first_name(),
            'last_name': faker.fake.last_name(),
            'email': faker.fake.email()
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list
