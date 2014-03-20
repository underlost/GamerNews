from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView

from core.models import Account as User
from django_comments.models import Comment
from threadedcomments.models import ThreadedComment
from news.models import Blob, BlobInstance

def user_profile(request, username):
    account = get_object_or_404(Account, username=username)
    variables = RequestContext(request, {'user_obj': account, })
    return render_to_response(['profile/user_profile.html'], variables)

class BlobsforUser(ListView):
    paginate_by = 20
    template_name = 'profile/user_blobs.html'

    def get_queryset(self):
        self.u = get_object_or_404(Account, username=self.kwargs.pop('username'))
        return Blob.objects.filter(user__username=self.u).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super(BlobsforUser, self).get_context_data(**kwargs)
        context.update({'user_obj': self.u})
        return context

class CommentsforUser(ListView):
    paginate_by = 20
    template_name = 'profile/user_comments.html'

    def get_queryset(self):
        self.u = get_object_or_404(User, username=self.kwargs.pop('username'))
        return ThreadedComment.objects.filter(user__username=self.u).order_by('-submit_date')

    def get_context_data(self, **kwargs):
        context = super(CommentsforUser, self).get_context_data(**kwargs)
        context.update({'user_obj': self.u})
        return context
