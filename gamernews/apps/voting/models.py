from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from datetime import datetime

from .managers import VoteManager

vote_types = {
    1 : _(u"upvote"),
    0  : _(u"blank"),
    -1  : _(u"downvote"),
}

class Vote(models.Model):
    # A vote on an object by a User.
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    
    direction = models.SmallIntegerField(choices=vote_types.items(), default=1)
    timestamp = models.DateTimeField(editable=False, default=datetime.now)
    
    is_archived = models.BooleanField(default=False)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)

    def __unicode__(self):
        return u"%s on %s by %s" % (self.direction, self.object, self.user.username)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1
