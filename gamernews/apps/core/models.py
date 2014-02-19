import datetime
from hashlib import md5

from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from timezone_field import TimeZoneField
from gamernews.utils.user_functions import generate_secret_token

GENDER_CHOICES = (
	('F', _('Female')),
	('M', _('Male')),
	('P', _('Pirate')),
	('N', _('Ninja')),
	('R', _('Robot')),
)

class Account(AbstractUser):
		
	#Profile Settings
	about			  = models.TextField(blank=True)
	gender			  = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	location 		  = models.CharField(max_length=255, blank=True)
	url				  = models.URLField(max_length=500, blank=True)

	#Settings
	hide_mobile       = models.BooleanField(default=False)
	last_seen_on      = models.DateTimeField(default=datetime.datetime.now)
	last_seen_ip      = models.CharField(max_length=50, blank=True, null=True)
	preferences       = models.TextField(default="{}")
	view_settings     = models.TextField(default="{}")
	send_emails       = models.BooleanField(default=False)
	is_beta			  = models.BooleanField(default=True)
	timezone          = TimeZoneField(default="US/Pacific")
	secret_token      = models.CharField(max_length=12, blank=True, null=True)
	
	class Meta:
		db_table = 'Account'
		
	def save(self, *args, **kwargs):
		if not self.secret_token:
			self.secret_token = generate_secret_token(self.username, 12)
		super(Account, self).save(*args, **kwargs)