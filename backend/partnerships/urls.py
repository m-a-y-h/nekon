from rest_framework.routers import DefaultRouter
from .views import PartnerViewSet, ShareViewSet

router = DefaultRouter()
router.register('partners', PartnerViewSet)
router.register('shares', ShareViewSet)

urlpatterns = router.urls
