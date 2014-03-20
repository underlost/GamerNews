import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify

APPROVED_FEED='A'
DENIED_FEED='D'
PENDING_FEED='P'
DELETED_FEED='F'

STATUS_CHOICES = (
	(PENDING_FEED, 'Pending'),
	(DENIED_FEED, 'Denied'),
	(APPROVED_FEED, 'Approved'),
)

class Feed(models.Model):
	title = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500)
	public_url = models.URLField(max_length=500)
	feed_url = models.URLField(unique=True, max_length=500)
	is_defunct = models.BooleanField(default=False)
	approval_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING_FEED)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='owned_feeds')
	date_added = models.DateTimeField(verbose_name=_("When Feed was added to the site"), auto_now_add=True)

	def __unicode__(self):
		return self.title

	def save(self, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super(Feed, self).save(**kwargs)

	class Meta:
		ordering = ("title",)
