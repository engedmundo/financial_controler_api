from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.core.views import MyLoginView, MyLogoutView
from apps.core.views.home_view import home_view

urlpatterns = [
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "",
        home_view,
        name="home",
    ),
    path(
        "login/",
        MyLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        MyLogoutView.as_view(),
        name="logout",
    ),
]
