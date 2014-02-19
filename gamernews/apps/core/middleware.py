import datetime
import re
import random
import time
import logging
import operator

from django.http import HttpResponse
from django.conf import settings
from django.utils.cache import patch_vary_headers

from .utils import get_domain

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')

UNSET = object()

class MultipleProxyMiddleware(object):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()

class LastSeenMiddleware(object):
    def process_response(self, request, response):
        if ((request.path == '/' or
             request.path.startswith('recent/'))
            and hasattr(request, 'user')
            and request.user.is_authenticated()): 
            hour_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
            ip = request.META.get('HTTP_X_REAL_IP', None) or request.META['REMOTE_ADDR']
            request.user.last_seen_on = datetime.datetime.utcnow()
            request.user.last_seen_ip = ip
            request.user.save()
        return response
        
class TimingMiddleware:
    def process_request(self, request):
        setattr(request, 'start_time', time.time())