from django.conf.urls import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	#Admin
	url(r'^admin42/', include(admin.site.urls)),

	#Static
	url(r'^about/$', TemplateView.as_view(template_name="static/about.html")),
	url(r'^terms/$', TemplateView.as_view(template_name="static/terms.html")),
	url(r'^privacy/$', TemplateView.as_view(template_name="static/privacy.html")),
	url(r'^faq/$', TemplateView.as_view(template_name="static/faq.html")),
	url(r'^guidelines/$', TemplateView.as_view(template_name="static/guidelines.html")),

	#Profile
	url(r'user/', include('gamernews.apps.profile.urls', namespace="Profile",)),
	url(r'^', include('gamernews.apps.threadedcomments.urls')),
	url(r'^comments/', include('gamernews.vendor.django_comments.urls')),
	url(r'^', include('gamernews.apps.core.urls', namespace="Core",)),
	url(r'^', include('gamernews.apps.news.urls')),
)

if settings.DEBUG:
	#Static Media
	urlpatterns += patterns('',
	    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
	        'document_root': settings.STATIC_ROOT,
	    }),
	)
