from django.conf.urls import *

from voting.views import vote_on_object

from .models import ThreadedComment
from . import views

blob_dict = {
	'model': ThreadedComment,
	'template_object_name': 'comment',
	'allow_xmlhttprequest': True,
	'post_vote_redirect': '',
	'template_name': 'blobs/single_blob.html'
}

urlpatterns = patterns('',
	url(r'^u/(?P<username>[\w-]+)/comments/$', views.CommentsforUser.as_view(), name = "comments-by-user"),
	url(r'^comment/(?P<id>.*)/$', views.single_comment, name='single_comment'),
)
