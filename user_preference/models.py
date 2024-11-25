# these are standard imports
from datetime import datetime, date

# these are the django imports

from django.db import models
from django.conf import settings

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# these are the local imports
from tables.models import GeneralTable


# Create your models here.


def positive_decimal(value):
    if value is not None and value < 0:
        raise ValidationError(f"{value}is not a positive number. Value must be positive")
    return value


class Preference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="preference")

    gender = models.CharField(max_length=10, blank=True, null=True)
    
    min_age = models.PositiveIntegerField(blank=True, null=True)
    max_age = models.PositiveIntegerField(blank=True, null=True)

    min_height = models.PositiveIntegerField(blank=True, null=True)
    max_height = models.PositiveIntegerField(blank=True, null=True)

    min_weight = models.PositiveIntegerField(blank=True, null=True)
    max_weight = models.PositiveIntegerField(blank=True, null=True)

    min_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, validators=[positive_decimal])
    max_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, validators=[positive_decimal])

    preferred_location = models.CharField(max_length=100, blank=True, null=True)
    preferred_education = models.CharField(max_length=100, blank=True, null=True)
    preferred_occupation = models.CharField(max_length=100, blank=True, null=True)
    preferred_religion = models.CharField(max_length=100, blank=True, null=True)
    preferred_language = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # if self.min_age and self.max_age and self.min_age > self.max_age:
        #     raise ValidationError("Minimum age cannot be greater than maximum age.")
        # if self.min_height and self.max_height and self.min_height > self.max_height:
        #     raise ValidationError("Minimum height cannot be greater than maximum height.")
        # if self.min_weight and self.max_weight and self.min_weight > self.max_weight:
        #     raise ValidationError("Minimum weight cannot be greater than maximum weight.")
        # if self.min_income and self.max_income and self.min_income > self.max_income:
        #     raise ValidationError("Minimum income cannot be greater than maximum income.")
        
        # self.validate_preference_field(self.preferred_location, 'location')
        # self.validate_preference_field(self.preferred_education, 'education')
        # self.validate_preference_field(self.preferred_occupation, 'profession')
        # self.validate_preference_field(self.preferred_religion, 'religion')
    
        if not self.gender:
            if self.user.gender == "Male":
                self.gender = "Female"
            elif self.user.gender == "Female":
                self.gender = "Male"
            else:
                self.gender = "Other"
        
        self.is_active = self.user.is_active

        super().save(*args, **kwargs)
    
    # def validate_preference_field(self, value, field_type):
    #     """Validates the field value against the GeneralTable."""
    #     if value:
    #         valid_values = GeneralTable.objects.filter(type=field_type).values_list('name', flat=True)
    #         if value not in valid_values:
    #             raise ValidationError(f"Invalid {field_type} '{value}'. Valid {field_type}s are: {', '.join(valid_values)}")
    #     return value

    def __str__(self):
        return f"{self.user.username}'s preference"





