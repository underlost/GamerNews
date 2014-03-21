import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from django_comments.forms import CommentForm
from .models import ThreadedComment

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class ThreadedCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    comment = forms.CharField(
        label=_('Comment'),
        widget=forms.Textarea(attrs={'class':'form-control',}),
        max_length=COMMENT_MAX_LENGTH
    )

    def __init__(self, target_object, parent=None, data=None, initial=None):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(ThreadedCommentForm, self).__init__(target_object, data=data, initial=initial)

    def get_comment_model(self):
        return ThreadedComment

    def get_comment_create_data(self):
        d = super(ThreadedCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        return d

ThreadedCommentForm.base_fields.pop('name')
ThreadedCommentForm.base_fields.pop('email')
ThreadedCommentForm.base_fields.pop('url')
