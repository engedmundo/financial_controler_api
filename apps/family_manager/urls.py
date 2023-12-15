from rest_framework.routers import DefaultRouter

from apps.family_manager.viewsets import FamilyViewSet

router = DefaultRouter()
router.register(r'families', FamilyViewSet, basename='family')

urlpatterns = router.urls