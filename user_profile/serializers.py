# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from .models import Profile
from tables.models import GeneralTable 

'''
These serializer is used for the profile model
'''

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    # email = serializers.EmailField(source='user.email')
    # phone_number = serializers.CharField(source='user.phone_number')


    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user','age' 'created_at', 'updated_at','email','phone_number']

    def validate_location(self, value):
        locations = GeneralTable.objects.filter(type='location').values_list('name', flat=True)
        if value not in locations:
            raise serializers.ValidationError(f"Invalid location. Valid values are: {', '.join(locations)}")
        return value

    def validate_religion(self, value):
        religions = GeneralTable.objects.filter(type='religion').values_list('name', flat=True)
        if value not in religions:
            raise serializers.ValidationError(f"Invalid religion. Valid values are: {', '.join(religions)}")
        return value

    def validate_mother_tongue(self, value):
        mother_tongues = GeneralTable.objects.filter(type='language').values_list('name', flat=True)
        if value not in mother_tongues:
            raise serializers.ValidationError(f"Invalid mother tongue. Valid values are: {', '.join(mother_tongues)}")
        return value

    def validate_marital_status(self, value):
        marital_statuses = GeneralTable.objects.filter(type='marital_status').values_list('name', flat=True)
        if value not in marital_statuses:
            raise serializers.ValidationError(f"Invalid marital status. Valid values are: {', '.join(marital_statuses)}")
        return value

    def validate_education(self, value):
        education_levels = GeneralTable.objects.filter(type='education').values_list('name', flat=True)
        if value not in education_levels:
            raise serializers.ValidationError(f"Invalid education level. Valid values are: {', '.join(education_levels)}")
        return value

    def validate_occupation(self, value):
        occupations = GeneralTable.objects.filter(type='profession').values_list('name', flat=True)
        if value not in occupations:
            raise serializers.ValidationError(f"Invalid occupation. Valid values are: {', '.join(occupations)}")
        return value
    
    # def validate_language(self, value):
    #     languages = GeneralTable.objects.filter(type='language').values_list('name', flat=True)
    #     if value not in languages:
    #         raise serializers.ValidationError(f"Invalid language. Valid values are: {', '.join(languages)}")
    #     return value    

    
    def get_profile_image(self,obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None
        