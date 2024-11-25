# these are the Standard imports
from datetime import datetime, date

# these are the django imports
from django.db import models
from django.conf import settings



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="profile")
    bio = models.TextField(max_length=500, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True,default="D:\\DJANGO_Project\\Matrimonial_sw\\user_icon.jpg")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    caste = models.CharField(max_length=100, blank=True, null=True)
    income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    location = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    mother_tongue = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    # language = models.CharField(max_length=100, blank=True, null=True)

    # MARITAL_STATUS_CHOICES = (
    #     ('single', 'Single'),
    #     ('married', 'Married'),
    #     ('divorced', 'Divorced'),
    #     ('widowed', 'Widowed'),
    #     ('separated', 'Separated'),
    # )
    marital_status=models.CharField(max_length=100, blank=True, null=True,default='single')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        if self.user.date_of_birth:
            today = date.today()
            birth_date = self.user.date_of_birth
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        return None
    
    def save(self, *args, **kwargs):
        self.is_active = self.user.is_active
        self.age = self.calculate_age()
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.user.username