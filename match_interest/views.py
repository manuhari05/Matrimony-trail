#these are rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

# these are django imports
from django.db.models import Sum ,Avg ,Count, Q
from django.shortcuts import get_object_or_404

# these are local imports
from .models import Match
from user.models import User
from tables.models import Subscription
from .serializers import MatchSerializer, DynamicMatchSerializer
# , FreeMatchSerializer, PremiumMatchSerializer, GoldMatchSerializer
from user.serializers import UserSerializer
from utils.match_score import calculate_match_score
from user_profile.serializers import ProfileSerializer
from user_profile.models import Profile

from notification.models import Notification



a_matches = Match.objects.all()
# Create your views here.

'''
These MatchAPIView is used to get the list of all matches and create a new match.
'''

class MatchAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Default permission for authenticated users
    '''
    This method is used to get the list of all matches
    Accepts:
        Authentications: user must be authenticated
    Returns:
        - 200 OK: List of matches or User's match interest
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the user has no match interest
    '''

    def get(self, request):
        """Allow Admins to list all matches."""
        if request.user.is_staff:  # Only Admins can view all matches
            
            serializer = MatchSerializer(a_matches, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.user.role.role == 'User':
            user = request.user

            matches = Match.objects.filter(user1=user)
            if matches.exists():
                serializer = MatchSerializer(matches, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            else:
                return Response({"detail": "No match interest found."}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
    
    '''
    These method is used to create a new match
    Accepts:
        Authentications: user must be authenticated for user1
        request data : User2 in the JSON data to create a new match

    Returns:
        - 201 Created: If the match is created successfully
        - 400 Bad Request: If the request data is invalid
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the user2 does not exist
        - 400 Bad Request: If the match already exists
    '''

    def post(self, request):
        """Allow Users to create a new match."""
        user1 = request.user
        user2 = request.data.get('user2')  # assuming user2 is sent as part of the request data
        
        # Check if user2 exists
        try:
            user2_instance = User.objects.get(username=user2)
        except User.DoesNotExist:
            return Response({"error": "{User2} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()  # Copy the request data to avoid modifying the original data
        data['user2'] = user2_instance.pk 
        
        if user1 == user2_instance:
            return Response({"error": "User1 and User2 cannot be the same."}, status=status.HTTP_400_BAD_REQUEST)
        # elif Match.objects.filter(user1=user1, user2=user2_instance).exists():
        #     return Response({"error": "Match already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        match_exists = Match.objects.filter(
            (Q(user1=user1) & Q(user2=user2_instance)) |
            (Q(user1=user2_instance) & Q(user2=user1))
        ).first()

        if match_exists:
            return Response({"error": "Match already exists."}, status=status.HTTP_400_BAD_REQUEST)


        serializer = MatchSerializer(data=data)
        

        
        if serializer.is_valid():
            serializer.save(user1=user1, user2=user2_instance)
            Notification.objects.create(
                user=user2_instance,
                message=f"You have a new match interest from {user1.username}."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    These method is used to update the match interest
    Accepts:
        Authentications: user must be authenticated for user1
        
    Returns:
        - 200 OK: If the match is updated successfully
        - 400 Bad Request: If the request data is invalid
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the match does not exist
    '''

        
    def patch(self, request, match_id):
        """Allow Users to deactivate a match (set is_active to False)."""
        try:
            match = Match.objects.get(id=match_id, user1=request.user)
        except Match.DoesNotExist:
            return Response({"error": "Match not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

        # Deactivate the match (set is_active to False)
        active = request.data.get('is_active')
        match.is_active = active
        Notification.objects.update(
                user=match.user2,
                message=f"{match.user1.username} has deactivated the match interest."
            )
        match.save()

        return Response(MatchSerializer(match).data, status=status.HTTP_200_OK)
    
    '''
    These method is used to delete a match or deactivate the user 
    Accepts:
        Authentications: user must be authenticated for user1

    Returns:
        - 204 No Content: If the match is deleted successfully
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the match does not exist
        - 400 Bad Request: If the user is not authorized to delete the match
    '''

    def delete(self, request, match_id):
        """Allow Admins to delete a match."""
        if request.user.is_staff:  # Admin check
            try:
                match = Match.objects.get(id=match_id)
                match.delete()
                return Response({"message": "Match deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Match.DoesNotExist:
                return Response({"error": "Match not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.role.role == 'User':
            try:
                match = Match.objects.get(id=match_id, user1=request.user)
                match.is_active = False
                Notification.objects.update(
                    user=match.user2,
                    message=f"{match.user1.username} has deactivated the match interest."
                )
                match.save()
                return Response({"message": "Match deactivated successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Match.DoesNotExist:
                return Response({"error": "Match not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)


class MatchViewByAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(a_matches, request)
            serializer = MatchSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        else:
            return Response({"error":"You are not authorized to view this page"},status=status.HTTP_403_FORBIDDEN)
    
'''
These MatchViewRequest is used to get the list of all matches interest request and update the status

'''
class MatchViewRequest(APIView):
    permission_classes = [IsAuthenticated]

    '''
    These method is used to get the list of all matches interest request
    Accepts:
        Authentications: user must be authenticated for user2
    Returns:
        - 200 OK: List of matches interest request
        - 403 Forbidden: If the user is not authenticated
    '''

    def get(self, request):
        if request.user.is_active:
            matches = Match.objects.filter(user2=request.user, status='Pending')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(matches, request)
            serializer = MatchSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:
            return Response({"error":"You are not authorized to view this page"}, status=status.HTTP_403_FORBIDDEN)

    '''
    These method is used to update the status of the match interest request received
    Accepts:
        Authentications: user must be authenticated for user2
        request data : status in the JSON data to update the status of the match interest request
    Returns:
        - 200 OK: If the status is updated successfully
        - 400 Bad Request: If the request data is invalid
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the match does not exist
        - 400 Bad Request: If the status is not valid

    '''


    def patch(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id, user2=request.user)
        except Match.DoesNotExist:
            return Response({"error": "Match not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in ['Accepted', 'Rejected']:
            return Response({"error": "Invalid status. Must be 'Accepted' or 'Rejected'."}, status=status.HTTP_400_BAD_REQUEST)
        
        match.status = new_status
        Notification.objects.create(user=match.user1, message=f"Your match interest has been {new_status.lower()} of {match.user2.username}.")
        match.save()

        return Response(MatchSerializer(match).data, status=status.HTTP_200_OK)
    



'''
These MatchViewByUser is used to get the list of all matches by the user
'''




class MatchViewBySubscription(APIView):
    permission_classes = [IsAuthenticated]
    
    def find_gender(self, user):
        if user.gender.gender == 'Male':
            return 'Female'
        elif user.gender.gender == 'Female':
            return 'Male'
        else:
            return 'Other'

    def get_matches_with_scores(self, user, potential_matches):
        """Calculate match scores for all potential matches and sort them"""
        scored_matches = []
        
        for potential_match in potential_matches:
            match_score = calculate_match_score(user, potential_match)
            scored_matches.append({
                'user': potential_match,
                'match_score': match_score
            })
        
        # Sort by match score in descending order
        return sorted(scored_matches, key=lambda x: x['match_score'], reverse=True)

    def get(self, request):
        if not request.user.is_active:
            return Response({"detail": "Inactive user"}, status=403)

        # Get the subscription details
        subscription_type = request.user.subscription.subscription
        subscription_instance = get_object_or_404(Subscription, subscription=subscription_type)
        subscription_details = subscription_instance.details

        # Get potential matches based on gender and active status with optimized queries
        potential_matches = User.objects.filter(
            gender__gender=self.find_gender(request.user),
            is_active=True
        ).select_related(
            'profile', 
            'gender', 
            'preference'
        )

        # Calculate scores and sort matches
        sorted_matches = self.get_matches_with_scores(request.user, potential_matches)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        
        # Paginate the sorted matches
        start = (int(request.GET.get('page', 1)) - 1) * paginator.page_size
        end = start + paginator.page_size
        paginated_matches = sorted_matches[start:end]

        # Get just the user objects for serialization
        users_to_serialize = [match['user'] for match in paginated_matches]
        
        # Serialize the data
        serializer = DynamicMatchSerializer(
            users_to_serialize,
            many=True,
            context={
                'subscription_details': subscription_details,
                'request': request
            }
        )

        # Add match scores to the serialized data
        serialized_data = serializer.data
        for i, item in enumerate(serialized_data):
            item['match_score'] = round(paginated_matches[i]['match_score'], 2)

        # Create custom pagination response
        return Response({
            'count': len(sorted_matches),
            'next': f'?page={int(request.GET.get("page", 1)) + 1}' if end < len(sorted_matches) else None,
            'previous': f'?page={int(request.GET.get("page", 1)) - 1}' if start > 0 else None,
            'results': serialized_data
        })

'''
These ViewMatchProfiles is used to get the list of all details of the match profile by the user
'''

class ViewMatchProfiles(APIView):
    permission_classes = [IsAuthenticated]
    '''
    These method is used to get the list of all details of the match profile by the user
    Accepts:
        Authentications: user must be authenticated
    Returns:
        - 200 OK: List of matches
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the match does not exist
        - 400 Bad Request: If the match status is not 'Accepted'
    '''

    def get(self, request, match_id):
        # Retrieve the match by its ID
        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return Response({"error": "Match not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the match status is 'accepted'
        if match.status != 'Accepted':
            return Response({"error": "Match has not been accepted yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the authenticated user is part of the match
        if match.user1 != request.user and match.user2 != request.user:
            return Response({"error": "You are not a participant in this match."}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the profiles of both users
        try:
            if match.user1 == request.user:
                opposite_user_profile = Profile.objects.get(user=match.user2)
            elif match.user2 == request.user:
                opposite_user_profile = Profile.objects.get(user=match.user1)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found for the opposite user."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the profile
        opposite_user_profile_serializer = ProfileSerializer(opposite_user_profile)

        # Return the profile data
        return Response(opposite_user_profile_serializer.data, status=status.HTTP_200_OK)


# class MatchViewBySubscription(APIView):
#     permission_classes = [IsAuthenticated]

    
#     '''
#     These function is used to find the opposite gender of the user
#     '''

#     def find_gender(self, user):
#         if user.gender.gender == 'Male':
#             return 'Female'
#         elif user.gender.gender == 'Female':
#             return 'Male'
#         else:
#             return 'Other'
        
#     '''
#     These method is used to get the list of all matches by the user
#     Accepts:
#         Authentications: user must be authenticated
#     returns:
#         - 200 OK: List of matches
#         - 403 Forbidden: If the user is not authenticated
#         - 404 Not Found: If the user is not found
#         - 400 Bad Request: If the user is not active
#     '''

#     def get(self, request):
#         # Ensure the user is active
#         if not request.user.is_active:
#             return Response({"detail": "Inactive user"}, status=403)

#         # Get the subscription details from the user's subscription
#         subscription_type = request.user.subscription.subscription
#         try:
#             subscription_instance = Subscription.objects.get(subscription=subscription_type)
#         except Subscription.DoesNotExist:
#             return Response({"detail": "Subscription type not found"}, status=404)

#         subscription_details = subscription_instance.details

#         # Get the profile and user fields dynamically
#         profile_fields = subscription_details.get('profile_fields', [])
#         user_fields = subscription_details.get('user_fields', [])
#         print(profile_fields)
#         print(user_fields)

#         # Get the matches based on the user's gender
#         matches = User.objects.filter(gender__gender=self.find_gender(request.user))

#         # Apply pagination
#         paginator = PageNumberPagination()
#         paginator.page_size = 10
#         result_page = paginator.paginate_queryset(matches, request)

#         # Use the dynamic serializer to display the correct fields based on subscription details
#         serializer = DynamicMatchSerializer(
#             result_page, 
#             many=True, 
#             subscription_details=subscription_details  # Pass subscription details to the serializer
#         )

#         return paginator.get_paginated_response(serializer.data)



# class MatchViewBySubscription(APIView):
#     permission_classes = [IsAuthenticated]

#     def find_gender(self, user):
#         if user.gender.gender == 'Male':
#             return 'Female'
#         elif user.gender.gender == 'Female':
#             return 'Male'
#         else:
#             return 'Other'

#     def get(self, request):
#         print(request.user.gender)
#         if request.user.is_active and request.user.subscription.subscription == 'FREE':
#             matches = User.objects.filter(gender__gender = self.find_gender(request.user))
#             paginator = PageNumberPagination()
#             paginator.page_size = 10
#             result_page = paginator.paginate_queryset(matches, request)
#             serializer = FreeMatchSerializer(result_page, many=True)
#             return paginator.get_paginated_response(serializer.data)
        
#         elif request.user.is_active and request.user.subscription.subscription == 'PREMIUM':
#             matches = User.objects.filter(gender__gender = self.find_gender(request.user))
#             paginator = PageNumberPagination()
#             paginator.page_size = 10
#             result_page = paginator.paginate_queryset(matches, request)
#             serializer = PremiumMatchSerializer(result_page, many=True)
#             return paginator.get_paginated_response(serializer.data)
        
#         elif request.user.is_active and request.user.subscription.subscription == 'GOLD':
#             matches = User.objects.filter(gender__gender = self.find_gender(request.user))
#             paginator = PageNumberPagination()
#             paginator.page_size = 10
#             result_page = paginator.paginate_queryset(matches, request)
#             serializer = GoldMatchSerializer(result_page, many=True)
#             return paginator.get_paginated_response(serializer.data)

