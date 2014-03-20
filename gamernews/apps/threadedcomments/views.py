from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView

from gamernews.apps.core.models import Account as User
from gamernews.vendor.django_comments.models import Comment
from .models import ThreadedComment

def single_comment(request, id):
    comment = get_object_or_404(ThreadedComment, id=id)
    variables = RequestContext(request, {'comment': comment})
    return render_to_response('comments/single.html', variables)
