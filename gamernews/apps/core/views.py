import hashlib
import json

from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import cache
from django.template import RequestContext

from .forms import AccountForm, AccountModelForm, UserCreationForm
from .models import Account

def register(request):
    if not settings.ALLOW_NEW_REGISTRATIONS:
        messages.error(request, "The admin of this service is not "
                                "allowing new registrations.")
        return HttpResponseRedirect(reverse('aggregator:index'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('aggregator:index'))
    else:
        form = UserCreationForm()

    return TemplateResponse(request, 'core/register.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('index'))

def EditAccount(request):
	account = get_object_or_404(Account, username=request.user)
	f = AccountModelForm(request.POST or None, instance=account)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Changes saved.')
		return redirect('UserSettings')
	variables = RequestContext(request, {'form': f, 'user_obj': account,})
	return render_to_response('core/edit_profile.html', variables)

def AccountProfile(request, username):
	account = get_object_or_404(Account, username=username)
	variables = RequestContext(request, {'user_obj': account, })
	return render_to_response(['core/user_profile.html'], variables)