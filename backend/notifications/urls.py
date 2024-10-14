from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationTypeViewSet

router = DefaultRouter()
router.register('notifications', NotificationViewSet)
router.register('notification-types', NotificationTypeViewSet)

urlpatterns = router.urls
from django.urls import ( path, )
from rest_framework_simplejwt.views import ( TokenRefreshView, )

urlpatterns = []
