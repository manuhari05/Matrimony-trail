from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics


from .models import Profile
from .serializers import ProfileSerializer

from notification.models import Notification
'''
These ProfileCreateView and ProfileUpdateView are used to create and update the profile of a user.

'''

class ProfileCreateView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        """
        This method ensures that the profile is created with the authenticated user.
        The `user` field is set automatically when saving the profile.
        """
        serializer.save(user=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"Your profile has been created successfully."
        )

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    
    def get_object(self):
        # Get the Profile object for the currently authenticated user
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            # If no profile exists for the user, return None to trigger 404 error
            raise Profile.DoesNotExist
    
    def update(self, request, *args, **kwargs):
        # Get the profile object and update it
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        Notification.objects.create(
            user=self.request.user,
            message=f"Your profile has been updated successfully."
        )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
