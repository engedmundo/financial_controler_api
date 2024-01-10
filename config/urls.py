from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.account_manager.urls")),
    path("api/", include("apps.family_manager.urls")),
    path("api/", include("apps.financial_manager.urls")),
]
