from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "To access this page you need to login.")
            return redirect("login-page")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def del_session(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'working_day' in request.session.keys():
            del request.session['working_day']
        return view_func(request, *args, **kwargs)
    return wrapper_func
