# these are rest_framework imports
from rest_framework import serializers

# these are the django imports

from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import aauthenticate

# these are the local imports
from .models import User
from user_profile.serializers import ProfileSerializer

'''
These UserSerializer is used for user registration and user update
'''

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    class Meta:
        model = User
        # fields = ['username','password','date_of_birth','gender','role', 'first_name', 'last_name']
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password":e.messages})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            # Validate the new password using Django's validators
            try:
                validate_password(password, instance)
            except serializers.ValidationError as e:
                raise serializers.ValidationError({"password": e.messages})

            # If the password is updated, set the new password and flag it
            instance.set_password(password)
            instance.password_updated_at = timezone.now()
        instance.save()
        return instance
    
'''
These PasswordUpdateSerializer is used for password update
'''
class PasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_curent_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError("New password cannot be the same as the current password.")
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        try:
            validate_password(data['current_password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password":e.messages})
        
        user = self.context['request'].user
        user.password_update_at = timezone.now()
        

        
        return data

    # def validate_date_of_birth(self, value):

    #     role = self.initial_data.get('role', 'user')
    #     if role == 'admin':
    #         return value

    #     today = timezone.now().date()
    #     age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    #     if age < 18 or age > 55:
    #         raise serializers.ValidationError("Only users between the age of 18 and 55 are allowed to create an account.")
    #     return value
    
    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user