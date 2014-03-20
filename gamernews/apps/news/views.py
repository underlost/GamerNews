from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, Page, InvalidPage, EmptyPage
from django.views.generic.list import ListView

from core.models import Account
from threadedcomments.models import ThreadedComment
from voting.models import Vote
from voting.views import vote_on_object

from .forms import *
from .models import Blob, BlobInstance


def paginate(request, queryset, pagesize=30):
	paginator = Paginator(queryset, pagesize)
	try:
		pageno = int(request.GET.get('page', '1'))
	except ValueError:
		pageno = 1
	try:
		page = paginator.page(pageno)
	except (EmptyPage, InvalidPage):
		page = paginator.page(paginator.num_pages) #last page
	return page

def paginate_blobs(request, votes, blobs):
		page = paginate(request, votes, 8)
		object_ids = [ d['object_id'] for d in page.object_list ] #d = direction.
		blobs = blobs.filter(id__in=object_ids)
		return page, blobs

def order_blobs(request, sortorder, blobs, min_tv=0, subset=None):
	blob_ids = None
	if subset:
		blob_ids = blobs.values_list('id')

	#sort blob on their vote score value.
	def _sort_blobs(votes, blobs,):
		scores = [(v['score'], v['object_id'],) for v in votes.all()]
		#scores.sort()
		id_blob = dict((blob.id, blob) for blob in blobs)
		sorted_blobs = []
		for score, id in scores:
			blob = id_blob.get(id, False)
			if blob:
				sorted_blobs.append(blob)
		return sorted_blobs

	if sortorder == 'popular':
		blobs = Blob.objects.all().order_by('-timestamp')[:150]
		for blob in blobs:
			delta_in_hours = (int(datetime.datetime.now().strftime("%s")) - int(blob.timestamp.strftime("%s"))) / 3600
			blob.popularity = ((blob.score() - 1) / ((delta_in_hours + 2)**1.8))
		blobs = sorted(blobs, key=lambda x: x.popularity, reverse=True)

	elif sortorder == 'controversial':
		votes = Vote.objects.get_controversial(Blob, object_ids=blob_ids, min_tv=min_tv)
		return paginate_blobs(request, votes, blobs)
	elif sortorder == 'top':
		votes = Vote.objects.get_top(Blob, object_ids=blob_ids, min_tv=min_tv)
		page, blobs = paginate_blobs(request, votes, blobs)
		blobs = _sort_blobs(page.object_list, blobs)
		return page, blobs
	elif sortorder == 'unpopular':
		votes = Vote.objects.get_bottom(Blob, object_ids=blob_ids, min_tv=min_tv)
		page, blobs = paginate_blobs(request, votes, blobs)
		blobs = _sort_blobs(page.object_list, blobs)
	elif sortorder == 'newest':
		blobs = blobs.order_by('-timestamp')
	elif sortorder == 'random':
		blobs = blobs.filter(timestamp__gte=datetime.datetime.now()-timedelta(days=3)).order_by('?')[:30]
	elif sortorder == 'unseen':
		if request.user.is_authenticated():
			votes = Vote.objects.get_user_votes(request.user, Blob) #get user votes.
			votes = votes.values_list('object_id', )
			blobs = blobs.exclude(id__in=votes)
	else:
		blobs = Blob.objects.all().order_by('-timestamp')[:150]
		for blob in blobs:
			delta_in_hours = (int(datetime.datetime.now().strftime("%s")) - int(blob.timestamp.strftime("%s"))) / 3600
			blob.popularity = ((blob.score() - 1) / ((delta_in_hours + 2)**1.8))
		blobs = sorted(blobs, key=lambda x: x.popularity, reverse=True)
	return False, blobs

def blob_list(request, *args, **kwargs):
	template_name = kwargs.get('template_name', "news/blob_list.html")
	extra_context = kwargs.get('extra_context', dict())
	time_frame = kwargs.get('time', None)

	page = False

	if kwargs.has_key('blobs'):
		blobs = kwargs['blobs']
	else:
		blobs = Blob.objects.all()

	if time_frame:
		days = None
		if time_frame == "today":
			days = 1
		elif time_frame == "week":
			days = 7
		elif time_frame == "month":
			days = 30
		elif time_frame == "year":
			days = 365
		if days:
			blobs = blobs.filter(timestamp__gte=(datetime.datetime.now() - timedelta(days=days)))

	min_tv = kwargs.get('min_tv', 1)
	subset = kwargs.get('subset', None)
	page, blobs = order_blobs(request, kwargs['sortorder'], blobs, min_tv, subset)

	if not page:
		page = paginate(request, blobs)
		blobs = page.object_list

	context = {'current' : 'all_blobs'}
	context.update(extra_context)
	context.update({
		'blobs'  : blobs,
		'page' : page,
		'votedata' : Vote,
		'sortorder' : kwargs.get('sortorder', ''),
		'total_blobs' : Blob.active.count(),
		'total_votes' : get_user_votes(request)
	})

	c = RequestContext(request, context)
	t = loader.get_template(template_name)
	return HttpResponse(t.render(c))

def get_user_votes(request):
	if request.user.is_authenticated():
		votes = Vote.objects.get_user_votes(request.user, Model=Blob)
		votes = votes.filter(object_id__in=Blob.active.values_list('id',))
		return votes.count()
	return 0

def single_blob(request, id):
	blob = get_object_or_404(Blob, id=id)
	variables = RequestContext(request, {'blob': blob})
	return render_to_response('news/single_blob.html', variables)

def single_comment_for_blob(request, blob_id, comment_id):
	blob = get_object_or_404(Blob, id=blob_id)
	comment = get_object_or_404(ThreadedComment, id=comment_id)
	variables = RequestContext(request, {'blob': blob, 'comment': comment,})
	return render_to_response('news/single_comment.html', variables)


@login_required
def submit(request):
	if request.method == "POST":
		blob_form = BlobInstanceForm(request.user, request.POST)
		if blob_form.is_valid():
			blob_instance = blob_form.save(commit=False)
			blob_instance.user = request.user
			blob_instance.save()
			blob = blob_instance.blob
			blob.save()
			messages.add_message(request, messages.INFO, 'You have saved %s' % blob_instance.title)
			return redirect('single_link', id=blob_instance.id)
	else:
		initial = {}
		if "url" in request.GET:
			initial["url"] = request.GET["url"]
		if "title" in request.GET:
			initial["title"] = request.GET["title"].strip()

		if initial:
			blob_form = BlobInstanceForm(initial=initial)
		else:
			blob_form = BlobInstanceForm()

	#blobs_add_url = "http://news.underlost.net" + reverse(submit)
	bookmarklet = "javascript:window.location=%22http://news.underlost.net/submit/?url=%22+encodeURIComponent(document.location)+%22&title=%22+encodeURIComponent(document.title)"
	return render_to_response("news/submit.html", { "bookmarklet": bookmarklet, "blob_form": blob_form,}, context_instance=RequestContext(request))
