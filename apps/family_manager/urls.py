from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.family_manager.viewsets import MyFamilyViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        "my-family/",
        MyFamilyViewSet.as_view(),
        name="my_family",
    ),
]
urlpatterns += router.urls
