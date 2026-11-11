from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """Only lets users with one of the given roles open the view.

    Users who are not logged in are sent to the login page.
    Logged-in users with another role get a 403 page.

    Usage:
        from accounts.models import User
        from accounts.permissions import role_required

        @role_required(User.Role.ADMIN, User.Role.TRAINER)
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
