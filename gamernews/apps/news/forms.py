import re
import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from vendor.django_comments.forms import CommentForm

from .models import Blob, BlobInstance

class BlobInstanceForm(forms.ModelForm):

	url = forms.URLField(label = "URL", required=False, widget=forms.TextInput(attrs={"size": 120, "class": "form-control"}))
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 120, "class": "form-control"}))
	note = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control"}))

	def __init__(self, user=None, *args, **kwargs):
		self.user = user
		super(BlobInstanceForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = ['url', 'title', 'note']

	def clean(self):
		cleaned_data = super(BlobInstanceForm, self).clean()
		url = cleaned_data.get('url')
		if url and BlobInstance.objects.filter(blob__url=url, user=self.user).count() > 0:
			raise forms.ValidationError(_("You have already submitted this link."))
		return cleaned_data

	def save(self, commit=True):
		self.instance.url = self.cleaned_data['url']
		return super(BlobInstanceForm, self).save(commit)

	class Meta:
		model = BlobInstance
		exclude = ('blob', 'user', 'slug', 'saved',)


#Simplify comments form
class SimpleCommentForm(CommentForm):
	def get_comment_create_data(self):
		return dict(
			content_type = ContentType.objects.get_for_model(self.target_object),
			object_pk    = force_unicode(self.target_object._get_pk_val()),
			comment      = self.cleaned_data["comment"],
			submit_date  = datetime.datetime.now(),
			site_id      = settings.SITE_ID,
			is_public    = True,
			is_removed   = False,
		)

SimpleCommentForm.base_fields.pop('name')
SimpleCommentForm.base_fields.pop('email')
SimpleCommentForm.base_fields.pop('url')
