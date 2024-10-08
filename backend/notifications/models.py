from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class NotificationType(models.Model):
    name = models.CharField(max_length=50)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
