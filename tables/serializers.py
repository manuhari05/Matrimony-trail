
# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from .models import Role, Gender, Subscription, GeneralTable, HelpRequest


'''
These serializers are used to serialize the data from the Role, Gender, Subscription, and GeneralTable models.
They define the fields that should be included in the serialized data.
The Meta class specifies the model and the fields to be included in the serialized data.
The serializers are used in the views to convert the model instances to JSON data and vice versa.

'''
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'



class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = ['id', 'user', 'subject', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class GeneralTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralTable
        fields = '__all__'
        