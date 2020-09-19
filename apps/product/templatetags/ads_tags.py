from __future__ import unicode_literals

from django import template

from apps.product.models.ads import Advertisement


register = template.Library()


@register.filter
def get_ads(place):
    """
    function to get the `raw_html` of advertisement.
    :param `place` is string of `Advertisement.PlaceOptions`
    :return string `raw_html` or empty.
    """
    ads = Advertisement.objects.get_or_none(place=place)
    return ads.raw_html if ads else ''
