import datetime
from django.conf import settings
from django.shortcuts import redirect

class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get('last_activity'):
            last_activity = request.session.get('last_activity')
            now = datetime.datetime.now().timestamp()
            max_idle_time = settings.SESSION_COOKIE_AGE  # Gunakan waktu dari settings.py

            if now - last_activity > max_idle_time:
                request.session.flush()  # Hapus session
                return redirect('login_admin')

        request.session['last_activity'] = datetime.datetime.now().timestamp()
        return self.get_response(request)
