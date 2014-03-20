import logging
import feedparser
from time import strftime
from hashlib import md5
from datetime import datetime

from django.db import models, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

log = logging.getLogger(__name__)

class BlobManager(models.Manager):

	def published(self):
		return self.hidden().filter(timestamp__lte=datetime.datetime.now())

	def hidden(self):
		return super(BlobManager, self).get_query_set().filter(is_hidden=False)

	def create_or_update_by_url(self, url, **kwargs):
		try:
			item = self.get(url=url)

		except self.model.DoesNotExist:
			# Create a new item
			log.debug('Creating entry: %s', url)
			kwargs['url'] = url
			item = self.create(**kwargs)

		else:
			log.debug('Updating entry: %s', url)

			# Don't update the date since most feeds get this wrong.
			kwargs.pop('timestamp')

			for k,v in kwargs.items():
				setattr(item, k, v)
			item.save()

		return item


class ActiveManager(models.Manager):
    pass
