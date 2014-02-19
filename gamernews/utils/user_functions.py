import hashlib

from django.core.cache import cache
from django.utils.http import urlquote
from django.http import HttpResponseForbidden
from django.conf import settings

def generate_secret_token(phrase, size=12):
    """Generate a (SHA1) security hash from the provided info."""
    info = (phrase, settings.SECRET_KEY)
    return hashlib.sha1("".join(info)).hexdigest()[:size]

def admin_only(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if not request.user.is_staff:
                return HttpResponseForbidden()
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)