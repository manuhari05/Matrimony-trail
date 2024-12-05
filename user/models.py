# these are the django imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import RegexValidator




class ActiveManager(models.Manager):
    # def  get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)
    
    def  get_queryset(self):
        return super().get_queryset()
    
    def get_active(self):
        return self.get_queryset().filter(is_active=True)
    
    def get_inactive(self):
        return self.get_queryset().filter(is_active=False)
    
    def active_count(self):
        return self.get_active().count()

# Create your models here.

class User(AbstractUser):
    
    
    date_of_birth = models.DateField(blank=True, null=True)
    # gender_choices = [
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # ]
    gender = models.ForeignKey('tables.Gender', on_delete=models.SET_NULL, null=True, blank=True)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True,validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # role_choices = [
    #     ('A', 'Admin'),
    #     ('U', 'User'),
    # ]

    role=models.ForeignKey('tables.Role', on_delete=models.SET_NULL, null=True, blank=True,default="R2")

    subscription=models.ForeignKey('tables.Subscription', on_delete=models.SET_NULL, null=True, blank=True, default="S01")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Attech the custom manager to the model
    # objects=models.Manager() # default manager
    # active= ActiveManager()  # Custom manager for active products

    password_update_at = models.DateTimeField(blank=True, null=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):

        # if self.password:
        #     # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{self.password}")
        #     self.validate_password(self.password)

        if self.date_of_birth:
            today = timezone.now().date()
            age=today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

            if age < 18 or age > 55:
                raise ValidationError("Only users between the age of 18 and 55 are allowed to create an account.")
        # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{self.role}")  
        if self.role and self.role.role == 'Admin':
            self.is_superuser = True
            self.is_staff = True
            self.is_admin = True

        else:
            self.is_superuser = False
            self.is_staff = False
            self.is_admin = False

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.username}"




    # def clean(self):

    #     if self.role == 'A':
    #         return

    #     today = timezone.now().date()
    #     age=today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    #     if age < 18 or age > 55:
    #         raise ValidationError("Only users between the age of 18 and 55 are allowed to create an account.")
        
    #     def __str__(self):
    #         return self.username