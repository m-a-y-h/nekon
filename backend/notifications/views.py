from django.shortcuts import render
from rest_framework import viewsets
from .models import Notification, NotificationType
from .serializers import NotificationSerializer, NotificationTypeSerializer

# Create your views here.

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationTypeViewSet(viewsets.ModelViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer
