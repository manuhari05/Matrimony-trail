from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Preference
from .serializers import PreferenceSerializer

'''
These PreferenceListCreateView and PreferenceUpdateView are used to get the list of all preferences and create a new preference.

'''

class PreferenceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    serializer_class = PreferenceSerializer

    def get_queryset(self):
        """
        Return the preferences of the authenticated user only.
        """
        # The user can only see their own preferences
        return Preference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically associate the authenticated user with the preference.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a preference for the authenticated user.
        """
        # If needed, you can validate or modify the data before saving.
        return super().create(request, *args, **kwargs)


class PreferenceUpdateView(generics.RetrieveUpdateAPIView):
    """
    API view for updating the user's preference. Ensures that only the authenticated user can update their preference.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = PreferenceSerializer

    def get_object(self):
        """
        Ensures that the user can only update their own preference.
        """
        try:
            preference = Preference.objects.get(user=self.request.user)
            return preference
        except Preference.DoesNotExist:
            # If no preference exists for the user, raise a 404 error
            raise Preference.DoesNotExist
    
    def get_serializer_context(self):
        """
        Include the current user in the serializer context so that we can access it for validation.
        """
        context = super().get_serializer_context()
        context['user'] = self.request.user  # Pass the authenticated user to the serializer context
        return context

    def update(self, request, *args, **kwargs):
        """
        Override the update method to allow updating the user's preference.
        """
        preference = self.get_object()
        serializer = self.get_serializer(preference, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


