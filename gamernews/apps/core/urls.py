from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.conf import settings

from .forms import PasswordResetForm
from . import views

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'core/login.html',} , name='login'),

    # Password Change
    url(r'^account/password/$', 'password_change', {
        'template_name': 'core/account/password_change_form.html',
        'post_change_redirect': 'Core:password_change_done',
        'current_app': 'Core',
        'extra_context': {'account_settings': True,},
    }, name='password_change'),

    # Password Change Done
    url(r'^account/password/done/$', 'password_change_done', {
        'template_name': 'core/account/password_change_done.html',
        'current_app': 'Core',
        'extra_context': {'account_settings': True,},
    }, name='password_change_done'),

    # Password reset
    url(r'^password_reset/$', 'password_reset', {
          'template_name': 'core/account/password_reset/form.html',
          'email_template_name': 'core/account/password_reset/email.txt',
          'subject_template_name': 'core/account/password_reset/email_subject.txt',
          'password_reset_form': PasswordResetForm,
          'current_app': 'Core',
          'post_reset_redirect' : 'Core:password_reset_done',
        }, name='password_reset'
    ),

    # Password Reset Done
    url(r'^password_reset/done/$', 'password_reset_done', {
        'template_name': 'core/account/password_reset/done.html',
        'current_app': 'Core',
    }, name='password_reset_done'),

    # Password Reset confirm
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm', {
            'template_name': 'core/account/password_reset/confirm.html',
            'current_app': 'Core',
        }, name='password_reset_confirm',),

    # Password reset complete
    url(r'^password_reset/complete/$', 'password_reset_complete', {
        'template_name': 'core/account/password_reset/complete.html',
        'current_app': 'Core',
    }, name='password_reset_complete'),
)

urlpatterns += patterns('',
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^account/$', views.EditAccount, name='AccountSettings'),
)
