from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login


def login_required(need_admin=False, redirect_page='Companies list'):
    def admin_login_required(view_func):
        def wrapped(request, *args, **kwargs):
            if request.user.is_anonymous:
                path = request.build_absolute_uri()
                return redirect_to_login(path, '/users/login')
            else:
                if not need_admin or request.user.is_staff:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'Недостаточно прав!')
                    return redirect(redirect_page)
        return wrapped
    return admin_login_required
