# these are rest_framework imports

from rest_framework import serializers

# these are local import
from .models import Match
from user.models import User
from user_profile.models import Profile

'''
These is a serializer for the Match model
'''
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = ['user1']



'''
These are the serializers to specify the particular fields of the user based on the user's subscriptions

'''





class DynamicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = []

    def __init__(self, *args, **kwargs):
        # Get subscription details from context instead
        self.subscription_details = kwargs.get('context', {}).get('subscription_details', None)
        super().__init__(*args, **kwargs)
        
        if self.subscription_details:
            profile_fields = self.subscription_details.get('profile_fields', [])
            allowed_fields = []
            for field in profile_fields:
                if field in [f.name for f in Profile._meta.get_fields()]:
                    allowed_fields.append(field)
            self.Meta.fields = allowed_fields

class DynamicMatchSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    match_score = serializers.FloatField(read_only=True)

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        # Get subscription details from context
        self.subscription_details = kwargs.get('context', {}).get('subscription_details', None)
        super().__init__(*args, **kwargs)

        if self.subscription_details:
            user_fields = self.subscription_details.get('user_fields', [])
            if 'profile' in user_fields:
                user_fields.remove('profile')
            
            allowed_fields = []
            for field in user_fields:
                if field in [f.name for f in User._meta.get_fields()]:
                    allowed_fields.append(field)
            
            # Always include profile and match_score
            allowed_fields.extend(['profile', 'match_score'])
            self.Meta.fields = allowed_fields

    def get_profile(self, obj):
        try:
            serializer = DynamicProfileSerializer(
                obj.profile,
                context={'subscription_details': self.subscription_details}
            )
            return serializer.data
        except Profile.DoesNotExist:
            return None
# class DynamicProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = []  # Initially empty
 
#     def __init__(self, *args, **kwargs):
#         subscription_details = kwargs.pop('subscription_details', None)
#         super().__init__(*args, **kwargs)
#         if subscription_details:
#             profile_fields = subscription_details.get('profile_fields', [])
#             self.Meta.fields = profile_fields
 
# class DynamicMatchSerializer(serializers.ModelSerializer):
#     profile = DynamicProfileSerializer(read_only=True)
 
#     class Meta:
#         model = User
#         fields = ['id', 'username','profile']  # Include essential user fields initially
 
#     def __init__(self, *args, **kwargs):
#         subscription_details = kwargs.pop('subscription_details', None)
#         super().__init__(*args, **kwargs)
#         if subscription_details:
#             user_fields = subscription_details.get('user_fields', [])
#             for field in user_fields:
#                 if field in User._meta.get_fields():
#                     self.fields[field] = serializers.CharField()
#             self.fields['profile'] = DynamicProfileSerializer(
#                 read_only=True, subscription_details=subscription_details
#             )









# class FreeProfile(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['profile_picture','age','bio','height','weight']
# class FreeMatchSerializer(serializers.ModelSerializer):
#     profile = FreeProfile(read_only=True)
#     class Meta:
#         model = User
#         fields = ['usernam','first_name','last_name','profile']



# class PremiumProfile(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['profile_picture','age','bio','height','weight','marital_status','religion']
# class PremiumMatchSerializer(serializers.ModelSerializer):
#     profile = PremiumProfile(read_only=True)
#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','profile','email','phone_number']


# class GoldProfile(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['profile_picture','age','bio','height','weight','education','religion',
#                   'language','marital_status','caste','income','location','city','mother_tongue',
#                   'occupation','education']
# class GoldMatchSerializer(serializers.ModelSerializer):
#     profile = GoldProfile(read_only=True)
    
#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','profile','email','phone_number']

   

    

