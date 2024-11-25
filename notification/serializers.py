# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from .models import Notification

'''
These is a serializer for the Notification model
'''

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
