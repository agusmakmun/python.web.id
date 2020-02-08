import os
import pygeoip
from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings

from app_blog.utils.visitor import get_client_ip


ONLINE_THRESHOLD = getattr(settings, 'ONLINE_THRESHOLD', 60 * 15)
ONLINE_MAX = getattr(settings, 'ONLINE_MAX', 50)


def get_online_now(self):
    return User.objects.filter(id__in=self.online_now_ids or [])


class OnlineNowMiddleware(MiddlewareMixin):
    """
    Source: https://gist.github.com/dfalk/1472104
    Usage : {{ request.online_now }} or {{ request.online_now_ids }}

    Maintains a list of users who have interacted with the website recently.
    Their user IDs are available as ``online_now_ids`` on the request object,
    and their corresponding users are available (lazily) as the
    ``online_now`` property on the request object.
    """

    def process_request(self, request):
        # First get the index
        uids = cache.get('online-now', [])

        # Perform the multiget on the individual online uid keys
        online_keys = ['online-%s' % (u,) for u in uids]
        fresh = cache.get_many(online_keys).keys()
        online_now_ids = [int(k.replace('online-', '')) for k in fresh]

        # If the user is authenticated, add their id to the list
        if request.user.is_authenticated:
            uid = request.user.id
            # If their uid is already in the list, we want to bump it
            # to the top, so we remove the earlier entry.
            if uid in online_now_ids:
                online_now_ids.remove(uid)
            online_now_ids.append(uid)
            if len(online_now_ids) > ONLINE_MAX:
                del online_now_ids[0]

        # Attach our modifications to the request object
        request.__class__.online_now_ids = online_now_ids
        request.__class__.online_now = property(get_online_now)

        # Set the new cache
        cache.set('online-%s' % (request.user.pk,), True, ONLINE_THRESHOLD)
        cache.set('online-now', online_now_ids, ONLINE_THRESHOLD)


class LanguageMiddleware(MiddlewareMixin):
    """
    django translation middleware
    ref: https://github.com/codingforentrepreneurs/Guides/blob/master/all/Django_Translation.md
    """

    def process_request(self, request):
        geoipdb = os.path.join(settings.BASE_DIR, 'djangoblog/geoipdb/GeoIP.dat')
        gi = pygeoip.GeoIP(geoipdb)

        client_ip = get_client_ip(request)
        client_country_code = gi.country_code_by_name(client_ip).lower()

        if 'lang' in request.GET:
            translation.activate(request.GET.get('lang'))

        # '' is if under dev on local.
        elif client_country_code != 'id' or client_country_code != '':
            translation.activate('en')

        # for dev: translation.activate('en')
