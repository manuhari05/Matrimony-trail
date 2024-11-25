# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from .models import Message

'''
These serializer is used for the message model
'''

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender',)