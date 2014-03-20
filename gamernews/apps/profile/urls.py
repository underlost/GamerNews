from __future__ import absolute_import

from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = patterns('',
	url(r'^(?P<username>[\w-]+)/$', views.UserProfile, name='Profile'),
    url(r'^(?P<username>[\w-]+)/posts/$', views.BlobsforUser.as_view(), name = "Blobs"),
	url(r'^(?P<username>[\w-]+)/comments/$', views.UserComments.as_view(), name = "Comments"),
)
