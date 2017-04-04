from django.shortcuts import redirect
import re

ALLOWED_IPS = ['^127\.0\.0\.1$','^192\.168\.1\..+$', '^186\.67\.238\.28$']
def login_by_ip(view_func):
    def authorize(request, *args, **kwargs):
        user_ip = request.META['REMOTE_ADDR']
        for ip in ALLOWED_IPS:
            authenticated_by_ip = re.compile(ip).match(user_ip)
            if authenticated_by_ip:
                return view_func(request, *args, **kwargs)
        return redirect('login')
    return authorize