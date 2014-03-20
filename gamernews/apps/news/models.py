from datetime import datetime
from base64 import encodestring
import re
import urllib

from django.db import models
from django.core.cache import cache
from django.template.defaultfilters import slugify, striptags
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify

from core.models import Account
from news.managers import BlobManager, ActiveManager
from news.fields import AutoSlugField
from voting.models import Vote

blob_types = (
    (u"job", _(u"Job")),
    (u"ask", _(u"Ask")),
    (u"default", _(u"Default")),
)

class Blob(models.Model):
    url = models.URLField(blank=True)
    title = models.CharField(_('title'), max_length=510)
    slug = models.SlugField(unique_for_date='timestamp')
    note = models.TextField(_('note'), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="added_blobs", verbose_name=_('user'))
    timestamp = models.DateTimeField(_('timestamp'), default=datetime.now)
    is_hidden = models.BooleanField(default=False)

    #Admin only
    type = models.CharField(choices=blob_types, max_length=25, default='default')

    def all_tags(self, min_count=False):
        return Tag.objects.usage_for_model(BlobInstance, counts=False, min_count=None, filters={'blob': self.id})

    def all_tags_with_counts(self, min_count=False):
        return Tag.objects.usage_for_model(BlobInstance, counts=True, min_count=None, filters={'blob': self.id})

    def score(self):
        votes = Vote.objects.filter(object_id=self.id)
        return sum(votes.values_list('direction', flat=True))

    #Ignore these managers for now.
    objects = BlobManager()
    active = ActiveManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/id/%s/" % (self.id)

	def save(self, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Blob, self).save(**kwargs)

    class Meta:
        ordering = ('-timestamp',)
        db_table = 'news_blobs'


class BlobInstance(models.Model):

    blob = models.ForeignKey(Blob, related_name="saved_instances", verbose_name=_('blob'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="saved_blobs", verbose_name=_('user'))
    timestamp = models.DateTimeField(_('saved'), default=datetime.now)
    title = models.CharField(_('title'), max_length=510)
    slug = models.SlugField(unique_for_date='timestamp')

    note = models.TextField(_('note'), blank=True)

    def _create_blob(self):
        blob = Blob(url=self.url, title=self.title, slug=self.slug, note=self.note, user=self.user)
        blob.save()
        return blob

    def save(self, force_insert=False, force_update=False):
    	if not self.id:
    		self.slug = slugify(self.title)

        if self.url:
            try:
                blob = Blob.objects.get(url=self.url)
            except Blob.DoesNotExist:
                blob = self._create_blob()
        else:
            blob = self._create_blob()

        self.blob = blob
        super(BlobInstance, self).save(force_insert, force_update)

    def delete(self):
        blob = self.blob
        super(BlobInstance, self).delete()
        if blob.saved_instances.all().count() == 0:
            blob.delete()

    def __unicode__(self):
        return _("%(blob)s for %(user)s") % {'blob':self.blob, 'user':self.user}

    class Meta:
        db_table = 'news_blobinstances'
