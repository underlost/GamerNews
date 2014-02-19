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

@register.simple_tag
def active(request, name, by_path=False):
	if by_path:
		path = name
	else:
		path = reverse(name)

	if request.path == path:
		return ' active '

	return ''
	
@register.filter
def adjust_for_pagination(value, page):
	value, page = int(value), int(page)
	adjusted_value = value + ((page - 1) * settings.RESULTS_PER_PAGE)
	return adjusted_value
