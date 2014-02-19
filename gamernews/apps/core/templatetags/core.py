import hashlib
from django import template
from string import Template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from urlparse import urlparse
from django.shortcuts import redirect, render, get_object_or_404

from gamernews.apps.core.models import Account

register = template.Library()

@register.filter
def base_site_url(value):                                        
	parsed = urlparse(value)
	return parsed.netloc

@register.filter
def email_hash(value):
	u = get_object_or_404(Account, username=value)
	a = hashlib.md5(u.email).hexdigest()                                       
	return a