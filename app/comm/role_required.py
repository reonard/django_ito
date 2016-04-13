# -*- coding: utf-8 -*-
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs

from django.utils.six.moves.urllib.parse import urlparse
from app.ticketmgr.models import Incident, Problem


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, *args):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def role_required(role, ticket_type, login_url):
    def check_permission(user, incident_id):
        if ticket_type == "incident":
            _class = Incident
        elif ticket_type == "problem":
            _class = Problem

        if role == "creator":
            role_username = _class.objects.get(pk=incident_id).creator.username
        elif role == "owner":
            role_username = _class.objects.get(pk=incident_id).owner.username
        else:
            role_username = ""
        print user.username

        if role_username == user.username or (user.is_staff and user.is_active):
            return True
        else:
            return False
    return user_passes_test(check_permission, login_url=login_url)


