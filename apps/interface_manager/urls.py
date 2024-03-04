from django.urls import path

from apps.interface_manager.views.login_view import LoginView

urlpatterns = [
    path(
        "",
        LoginView.as_view(),
        name="login",
    ),
]