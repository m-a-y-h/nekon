"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

api_patterns = [
    path('apis/', include('accounts.urls')),
    path('apis/', include('acc_and_prof_management.urls')),
    path('apis/', include('delivery.urls')),
    path('apis/', include('health_profiles.urls')),
    path('apis/', include('notifications.urls')),
    path('apis/', include('orders.urls')),
    path('apis/', include('partnerships.urls')),
    path('apis/', include('payments.urls')),
    path('apis/', include('profiles.urls')),
    path('apis/', include('search_and_discovery.urls')),
]

urlpatterns = [
    path('', include(api_patterns)),
    path('admin/', admin.site.urls),
]