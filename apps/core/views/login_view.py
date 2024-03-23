from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("home")
