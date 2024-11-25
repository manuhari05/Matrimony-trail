
# these are the django imports
from django.db import models

# these are the local imports 
from user.models import User
from utils.match_score import calculate_match_score

# Create your models here.

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user1_matches')
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user2_matches')
    status = models.CharField(max_length=20, 
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], 
                              default='pending')
    
    match_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
   
        self.match_score = calculate_match_score(self.user1, self.user2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username} - {self.status}"
