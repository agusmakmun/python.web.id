from __future__ import unicode_literals

import re
import ast
import hashlib
from django import template
from django.utils.module_loading import import_string

try:
    # Python 3
    from urllib.parse import (urlencode, urlparse, parse_qs)
except ImportError:
    # Python 2
    from urllib import (urlencode, urlparse, parse_qs)

register = template.Library()


@register.filter
def splitter(value, sep='.'):
    """
    return splited list.
    :param `value` is value to split.
    :param `sep` is splitter.

    usage:
        {{ value|splitter:"/" }}
    """
    return value.split(sep)


@register.filter
def gravatar(email, size="75"):
    """
    return gravatar url.
    :param `email` is email from user.
    :param `size` is string size of image.

    usage:
        {{ request.user.email|gravatar:"75" }}
    """
    gravatar_url = "//www.gravatar.com/avatar/" + \
        hashlib.md5(email.encode('utf-8')).hexdigest() + "?"
    gravatar_url += urlencode({'d': 'retro', 's': str(size)})
    return gravatar_url


@register.filter
def wordsonly(value):
    """
    return string words only.
    :param `value` is value from text or words.

    usage:
        {{ post.description|striptags|truncatewords:"20"|wordsonly }}
    """
    return re.sub(r'[^\w\s]', '', value, flags=re.I | re.M)


@register.filter
def numberize(number):
    """
    return convert number to string, an example:
        - 1000 to 1k
        - 1000000 to 1m, etc.
    :param `number` is number to convert.

    usage:
        {{ post.get_visitors.count|numberize }}
    """
    if type(number) == int:
        if number > 999 and number <= 999999:
            return "{0:.1f}k".format(number / 1000)
        elif number > 999999 and number <= 999999999:
            return "{0:.1f}m".format(number / 1000000)
        elif number > 999999999 and number <= 999999999999:
            return "{0:.1f}b".format(number / 1000000000)
        elif number > 999999999999 and number <= 999999999999999:
            return "{0:.1f}t".format(number / 1000000000000)
        else:
            return "{}".format(number)
    return "{}".format(number)


@register.filter
def has_group(user, mode='single'):
    """
    return group/s object/s from user.
    :param `user` is user object.
    :param `mode` is single/plural mode.

    single:
        {{ request.user|has_group }}

    plural:
        {{ request.user|has_group:"plural" }}
    """
    if mode.lower() == 'plural':
        return user.groups.all()
    return user.groups.first()


@register.filter
def counter(model_name, filter=None):
    """
    by all objects:
        {{ 'yourapp.model.ClassName'|counter }}

    by filter objects:
        {{ 'yourapp.model.ClassName'|counter:"{'field_name':'value'}" }}

    bug:
        http://stackoverflow.com/q/42245164/6396981
    """
    model = import_string(model_name)
    if filter is not None:
        filter_dict = ast.literal_eval(filter)
        return model.objects.filter(**filter_dict).count()
    return model.objects.count()


@register.filter
def get_tuple_value(tuples, key):
    """
    an example tuples for:
        tuples = (
            ("1", "Afghanistan"),
            ("2", "Albania"),
            ("3", "Algeria")
        )
    :param `tuples` is tuples inside tuple.
    :param `key` is the key from per-single tuple.

    usage:
        {{ tuples|get_tuple_value:"1" }}
    """
    for k, v in tuples:
        if k == key:
            return v
    return key


@register.filter
def markdown_find_images(markdown_text):
    """
    return list of image urls inside `markdown_text`.
    :param `markdown_text` is markdown text to find.

    example markdown text:
        Hello ![title](/path/to/image.png)

    provides for:
        jpeg|jpg|png|gif

    demo:
        https://goo.gl/3LEXom

    usage:
        {{ field_name|markdown_find_images }}

    example:
        {{ post.description|markdown_find_images }}
    """
    # findgex = r"[^(\s]+\.(?:jpeg|jpg|png|gif)(?=\b[+^\)])"
    findgex = r"[^(\s]+\.(?:jpeg|jpg|png|gif)(?=\))"
    return re.findall(findgex, markdown_text)


@register.filter
def get_youtube_video_id(url):
    """
    Returns Video_ID extracting from the given url of Youtube

    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
        'https://www.youtube.com/watch?v=S6q41Rfltsk'

      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA'

    usage:
        {{ youtube_url|get_youtube_video_id }}

    Source: https://gist.github.com/kmonsoor/2a1afba4ee127cce50a0
    """
    if url.startswith(('youtu', 'www')):
        url = 'http://' + url

    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError
