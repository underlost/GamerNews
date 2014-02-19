from django.conf.urls import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from gamernews.apps.core import views as core_views
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
			
	#Core
	url(r'^register/$', core_views.register, name='registration_register'),
	url(r'^logout/$', core_views.logout_user, name='logout'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
	url(r'^login/password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'core/password_reset_form.html'}, name='password_reset'),
	url(r'^login/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^login/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		'django.contrib.auth.views.password_reset_confirm', {'template_name': 'core/password_reset_confirm.html'}, name='password_reset_confirm'),
	url(r'^login/reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'core/password_reset_complete.html'}, name='password_reset_complete'),
	#Settings
	url(r'^settings/$', core_views.EditAccount, name='UserSettings'),
	url(r'^settings/password/$', 'django.contrib.auth.views.password_change', {'template_name': 'core/password_change_form.html'}, name='password_change'),
	url(r'^settings/password/done/$', 'django.contrib.auth.views.password_change_done', { 'template_name': 'core/password_change_done.html'}, name='password_change_done'),
	
	# Comments apps
	(r'^comments/', include('gamernews.vendor.django_comments.urls')),
	(r'^', include('gamernews.apps.threadedcomments.urls')),

	#News App
	url(r'^', include('gamernews.apps.news.urls')),
	
)

if settings.DEBUG:
	#Static Media
	urlpatterns += patterns('',
	    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
	        'document_root': settings.STATIC_ROOT,
	    }),
	)