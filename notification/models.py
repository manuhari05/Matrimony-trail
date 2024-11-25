# these are the django imports
from django.db import models

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}: {self.message}"