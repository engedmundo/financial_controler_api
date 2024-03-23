from django.contrib.auth.views import LogoutView


class MyLogoutView(LogoutView):
    next_page = "/login"
