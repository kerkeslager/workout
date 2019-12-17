import functools

from django.shortcuts  import redirect
from django.urls import reverse

def require_auth(view):
    @functools.wraps(view)
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect(reverse('authorization:log_in') + '?redirect=' + request.get_full_path())

        return view(request)

    return wrapper
