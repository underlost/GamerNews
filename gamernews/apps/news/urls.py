from django.conf.urls import *
from django.views.decorators.cache import cache_page

from .models import Blob
from . import views
from voting.views import vote_on_object


blob_dict = {
	'model': Blob,
	'template_object_name': 'blob',
	'allow_xmlhttprequest': True,
	'post_vote_redirect': '',
	'template_name': 'blobs/blob_list.html'
}

urlpatterns = patterns('',
	#Main
	url(r'^submit/$', views.submit, name='submit_form'),
	url(r'^blobs/(?P<object_id>.*)/(?P<direction>up|down|clear)vote/?$', vote_on_object, blob_dict),
	url(r'^id/(?P<blob_id>.*)/(?P<comment_id>.*)/$', views.single_comment_for_blob, name='single_comment_for_blob'),

	url(r'^id/(?P<id>.*)/$', views.single_blob, name='single_link'),
	url(r'^((?P<sortorder>newest|popular|controversial|unpopular|unseen|top|random)/)?((?P<time>today|week|month|year|all)/)?$', views.blob_list , name='blob_list'),


)
