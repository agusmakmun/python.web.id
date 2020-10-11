from __future__ import unicode_literals

import re
import json
import hashlib
from urllib import parse
from django import template

try:
    # Python 3
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode

register = template.Library()


@register.filter
def splitter(value, sep='.'):
    """
    return splitted list.
    :param `value` is value to split.
    :param `sep` is splitter.

    usage:
        {{ value|splitter:"/" }}
    """
    return value.split(sep)


@register.filter
def subtract(value, arg):
    """
    return value - arg

    {{ value|subtract:arg }}
    """
    return value - arg


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
    scales = {
        1000: 'k',
        1000000: 'm',
        1000000000: 'b',
        1000000000000: 't',
        1000000000000000: 'quad',
        1000000000000000000: 'quin',
        1000000000000000000000: 'sexti',
        1000000000000000000000000: 'septi',
        1000000000000000000000000000: 'octi',
        1000000000000000000000000000000: 'noni',
        1000000000000000000000000000000000: 'deci',
        1000000000000000000000000000000000000: 'undeci',
        1000000000000000000000000000000000000000: 'duodeci',
        1000000000000000000000000000000000000000000: 'trede',
        1000000000000000000000000000000000000000000000: 'quattu',
        1000000000000000000000000000000000000000000000000: 'quindeci',
        1000000000000000000000000000000000000000000000000000: 'sexdeci',
        1000000000000000000000000000000000000000000000000000000: 'septend',
        1000000000000000000000000000000000000000000000000000000000: 'octodeci',
        1000000000000000000000000000000000000000000000000000000000000: 'novemdeci',
        1000000000000000000000000000000000000000000000000000000000000000: 'vigintillion',
        1000000000000000000000000000000000000000000000000000000000000000000: 'infinity'
    }

    try:
        number = int(number)
    except ValueError:
        return number

    for digit, name in scales.items():
        minimum = '9' * len(str(digit)[1:])
        maximum = minimum + '999'

        if number > max(scales):
            return "{0:.1f} ".format(number / max(scales)) + name

        elif number > int(minimum) and number <= int(maximum):
            return "{0:.1f} ".format(number / digit) + name
    return number


@register.filter
def has_group(user, group_name):
    """
    return boolean
    :param `user` is user object.
    :param `group_name` is string group name.

    {{ request.user|has_group:"admin" }}
    """
    if hasattr(user, 'groups'):
        return group_name in user.groups.values_list('name', flat=True)
    return False


@register.filter
def has_perm(user, permission):
    """
    return boolean
    :param `user` is request.user
    :param `permission` is string permission

    {% if request.user|has_perm:"apps.add-cart" %}
      {# do_stuff #}
    {% endif %}
    """
    if user.is_anonymous:
        return False
    return user.has_perm(permission)


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
    items = dict(tuples)
    if key in items.keys():
        return items.get(key)
    return key


@register.filter
def is_exist(value, default=''):
    """
    function to show the value whenever it exist,
    if doesn't exist will return default value.
    :param `value` is object/string/number/etc value.
    :param `default` is default char/text to show if doesn't exist.
    """
    return value if value else default


@register.filter
def title_status(value):
    """
    function to change the string into title case,
    e.g: 'you and me' => 'You And Me'
    :param `value` is string value
    """
    if value:
        value = str(value)
        return value.replace('_', ' ').replace('-', ' ').title()
    return ''


@register.filter
def in_range(value):
    """
    function to convert the number into range,
    e.g: 10 => range(0, 10)
    :param `value` is integer value
    """
    return range(int(value))


@register.filter
def parse_json(json_data, indent=2):
    """
    function to outputing the json format with beautiful indent.
    :param `json_data` is like, {"a": 1} or '{"a": 1}'
    :param `indent` is indentation number.
    """
    try:
        if isinstance(json_data, dict):
            return json.dumps(json_data, indent=indent)
        return json.dumps(eval(json_data), indent=indent)
    except Exception:
        return json_data
    return None


@register.filter
def is_image_url(url):
    """
    function to check the url as image_url or not.
    :param `url` is image url.
    """
    image_extensions = ['.png', '.jpeg', '.jpg', '.gif']
    image_url = str(url).lower()
    for ext in image_extensions:
        if image_url.endswith(ext):
            return True
    return False


@register.filter
def digit_after_comma(int_float, max_digit=2):
    """
    parse eg: 32.352 to 32.35
              20     to 20.00
    :param `int_float` is integer float number.
    :param `max_digit` is total max digits after comma/dot.
    """
    if not int_float:
        return None

    try:
        int_float = float(int_float)
        pattern = '%' + '.%sf' % max_digit
        return float(pattern % int_float)
    except Exception as error:
        print(error)
        return int_float


@register.filter
def in_list(value, list_comma, pattern=','):
    """
    :param `value` is string text, eg: "you"
    :param `list_comma` is string text, eg: "you,and,me"
    :param `pattern` is split pattern in strin, e.g: ,

    {% if object.status|in_list:"pending,paid,bought" %}
      {# do_stuff #}
    {% endif %}
    """
    list_comma = str(list_comma)
    return value in list_comma.split(pattern)


@register.filter
def as_rupiah(nominal, replace_comma=False, comma=2):
    """
    >>> rupiah(10210031)
    '10,210,031'
    >>> rupiah(10210031, replace_comma=True)
    '10.210.031'
    >>>
    """
    try:
        if not nominal:
            return 0
        elif isinstance(nominal, float):
            nominal = float("%.2f" % nominal)
        elif isinstance(nominal, str):
            nominal = int(nominal)

        nominal = "{:,}".format(round(nominal, comma))

        if replace_comma:
            return nominal.replace(',', '.')
        return nominal

    except Exception:
        return nominal


@register.filter
def append_url_param(url, rep='lang=en'):
    """
    function to replace the query string of url.
    issue: https://stackoverflow.com/a/63561716/6396981
    :param `url` is string full url or GET query params.
    :param `rep` is string replacer.
    """
    rep_list = rep.split('=')
    queries = url

    if len(rep_list) > 1:
        rep_key = rep_list[0]
        rep_val = rep_list[1]

        if 'http' in url:
            queries = parse.urlsplit(url).query

        dict_params = dict(parse.parse_qsl(queries))
        dict_params.update({rep_key: rep_val})

        queries_list = []

        for (k, v) in dict_params.items():
            queries_list.append('%s=%s' % (k, v))

        base_url_list = url.split('?')
        base_url = base_url_list[0]

        if len(base_url_list) <= 1:
            base_url = ''

        queries_str = '&'.join(queries_list)

        return '%s?%s' % (base_url, queries_str)

    return url


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
