import re
# these are the django imports
from django.db import models
from django.utils import timezone
from django.db.models import Max


# Create your models here.
class Role(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    role = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role
    
class Gender(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    gender = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gender
    
class Subscription(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    subscription = models.CharField(max_length=50, unique=True)
    details = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subscription
    
class HelpRequest(models.Model):
    user = models.ForeignKey('user.User', related_name="help_requests", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255) 
    description = models.TextField()  
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ], default='open')
    created_at = models.DateTimeField(auto_now_add=True)  # When the request was created
    updated_at = models.DateTimeField(auto_now=True)  # Last time it was updated

    def __str__(self):
        return f"Help Request from {self.user.username} - {self.subject}"


    

class GeneralTable(models.Model):

    FIELD_TYPES = [
        ('marital_status','Marital Status'),
        ('language','Language'),
        ('education', 'Education'),
        ('religion', 'Religion'),
        ('caste', 'Caste'),
        ('location', 'Location'),
        ('profession', 'Profession'),

    ]

    type = models.CharField(max_length=50, choices=FIELD_TYPES)
    code = models.CharField(max_length=50, unique=True,blank=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            prefix = self.type[:2].upper()

            max_code = GeneralTable.objects.filter(type=self.type).aggregate(Max('code'))['code__max']

            if max_code:
                # Use regex to extract the numeric part after the prefix
                match = re.match(rf"^{prefix}(\d+)$", max_code)
                if match:
                    last_number = int(match.group(1))  # Extract the numeric part
                    new_number = last_number + 1
                    self.code = f"{prefix}{new_number:02d}"  # Format with two digits
                else:
                    self.code = f"{prefix}01"  # Default to starting from 01
            else:
                self.code = f"{prefix}01"  # Start from 01 if no previous code exists

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


    #         prefix = self.type[:2].upper()
        
    #         max_code = GeneralTable.objects.filter(type=self.type).aggregate(Max('code'))['code__max']

    #         if max_code:
    #             last_number = int(max_code[2:])
    #             new_number = last_number + 1
    #             self.code = f"{prefix}{new_number:02d}"

    #         else:
    #             self.code = f"{prefix}01"
        
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.name
