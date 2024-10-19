# your_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, LoginView, SearchView  # Correct import

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('api/acc-and-prof-management/', include(router.urls)),  # Router handles dishes here
    path('api/acc-and-prof-management/login/', LoginView.as_view(), name='login'),
    path('api/search/', SearchView.as_view(), name='search'),
]
