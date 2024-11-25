# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from tables.models import GeneralTable
from .models import Preference

'''
These serializer is used for the preference model
'''

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'
        read_only_fields = ['user']


    def validate(self, data):
        """
        Validate fields that depend on each other (like min/max values).
        """
        min_age = data.get('min_age')
        max_age = data.get('max_age')
        min_height = data.get('min_height')
        max_height = data.get('max_height')
        min_weight = data.get('min_weight')
        max_weight = data.get('max_weight')
        min_income = data.get('min_income')
        max_income = data.get('max_income')

        if min_age and max_age and min_age > max_age:
            raise serializers.ValidationError("Minimum age cannot be greater than maximum age.")
        
        if min_height and max_height and min_height > max_height:
            raise serializers.ValidationError("Minimum height cannot be greater than maximum height.")
        
        if min_weight and max_weight and min_weight > max_weight:
            raise serializers.ValidationError("Minimum weight cannot be greater than maximum weight.")
        
        if min_income and max_income and min_income > max_income:
            raise serializers.ValidationError("Minimum income cannot be greater than maximum income.")
        
        return data

    def validate_preference_field(self, value, field_type):
        """
        Validates the field value against the GeneralTable.
        """
        if value:
            valid_values = GeneralTable.objects.filter(type=field_type).values_list('name', flat=True)
            if value not in valid_values:
                raise serializers.ValidationError(f"Invalid {field_type} '{value}'. Valid {field_type}s are: {', '.join(valid_values)}")
        return value

    def validate_preferred_location(self, value):
        return self.validate_preference_field(value, 'location')

    def validate_preferred_education(self, value):
        return self.validate_preference_field(value, 'education')

    def validate_preferred_occupation(self, value):
        return self.validate_preference_field(value, 'profession')

    def validate_preferred_religion(self, value):
        return self.validate_preference_field(value, 'religion')
    
    def validate_preferred_language(self, value):
        return self.validate_preference_field(value, 'language')
    
    def validate_gender(self, value):
        """
        If gender is not provided, set it based on the user's gender.
        Assumes that the 'user' is passed in the context of the serializer.
        """
        # Get the user from the context
        user = self.context.get('user')

        # If no value is provided for gender, set it based on user's gender
        if not value:
            if user:
                print(user.gender)
                if str(user.gender) == "Male":
                    return "Female"
                elif str(user.gender) == "Female":
                    print(user.gender)
                    return "Male"
                else:
                    return "Other"
            else:
                raise serializers.ValidationError("User not found in context. Cannot determine gender.")
        
        return value