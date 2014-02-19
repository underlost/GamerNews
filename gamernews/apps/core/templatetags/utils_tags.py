import struct
from django.contrib.sites.models import Site
from django.conf import settings
from django import template
from vendor.timezones.utilities import localtime_for_timezone

register = template.Library()

@register.simple_tag
def current_domain(dev=False, strip_www=False):
    current_site = Site.objects.get_current()
    domain = current_site and current_site.domain
    if dev and settings.SERVER_NAME in ["dev"] and domain:
        domain = domain.replace("www", "dev")
    if strip_www:
        domain = domain.replace("www.", "")
    return domain