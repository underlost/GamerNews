from datetime import datetime

from django.db import models, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

class BlobManager(models.Manager):
	
	def published(self):
		return self.hidden().filter(timestamp__lte=datetime.datetime.now())
	
	def hidden(self):
		return super(BlobManager, self).get_query_set().filter(is_hidden=False)

class ActiveManager(models.Manager):
    pass
       