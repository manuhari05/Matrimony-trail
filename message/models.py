# these are the django imports
from django.db import models

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='received_messages')
    message = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.message}"
   
