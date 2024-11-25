# from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from django.utils import timezone
from django.contrib.auth import authenticate
from django.db.models import Sum ,Avg ,Count, Q


from .serializers import UserSerializer, PasswordUpdateSerializer
from .models import User

from notification.models import Notification
from message.models import Message



# Create your views here.


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        These method Handle user login with username and password.
        
        Accepts:
        {
            'username': 'string',
            'password': 'string'
        }
        
        Returns:
        - Token for authenticated user
        - Counts of unread notifications and messages
        """
        # Validate input data
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Use Django's built-in authentication
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user account is active
        if not user.is_active:
            return Response({
                'error': 'User account is inactive'
            }, status=status.HTTP_403_FORBIDDEN)

        # Create or get authentication token
        token, _ = Token.objects.get_or_create(user=user)

        # Update last login (optional, but recommended)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        # Count unread notifications and messages efficiently
        unread_notifications_count = Notification.objects.filter(
            user=user, 
            is_read=False
        ).count()

        unread_messages_count = Message.objects.filter(
            receiver=user, 
            is_read=False
        ).count()

        # Return response with token and counts
        return Response({
            'token': token.key,
            'unread_notifications': unread_notifications_count,
            'unread_messages': unread_messages_count
        }, status=status.HTTP_200_OK)
        

'''
This UserListCreateView is used to get the list of all the users and create a new user.

'''

class UserListCreateView(APIView):
    permission_classes = [IsAdminUser]
    class StandardResultsSetPagination(PageNumberPagination):
        page_size = 13  # You can adjust the page_size here
        page_size_query_param = 'page_size'  # Allow the client to specify page size
        max_page_size = 100

    
    '''
    This method is used to get the list of all the users

    Accepts: 
         request
    Returns:
         200_OK: if the request is successful
         400_BAD_REQUEST: if the request is not successful  
    '''

    def get(self, request):
        users = User.objects.all()
        
        # Apply pagination
        paginator = self.StandardResultsSetPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        
        # Serialize paginated users
        serializer = UserSerializer(paginated_users, many=True)
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


        # users = User.objects.all()
        # serializer = UserSerializer(users, many=True)
        # return Response(serializer.data,status=status.HTTP_200_OK)
    
    '''
    This method is used to create a new user
    Accepts:
        request data : JSON objects containing the data of the user to be created

    Returns:
        -  201_CREATED: if the request is successful
        -  400_BAD_REQUEST: if the request is not successful
    '''

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

'''
This UserDetailUpdateDeleteView is used to get the detail of a user, update the user and delete the user.

'''
    
class UserDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    '''
    This method is used to get the detail of a user
    Accepts:
        pk (int): primary key of the user

    Returns:
        -  200_OK: if the request is successful
        -  404_NOT_FOUND: if the request is not successful
        -  403_FORBIDDEN: if the request is not successful
    '''

    def get(self, request, pk):
        # Any authenticated user can view their own data
        try:
            user = User.objects.get(pk=pk)
            print(request.user.is_staff)
            if user != request.user and not request.user.is_staff:
                return Response({"detail": "You do not have permission to view this user."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    '''
    This method is used to update the user
    Accepts:
        pk (int): primary key of the user
        request data : JSON objects containing the data of the user to be updated
    
    Returns:
        -  200_OK: if the request is successful
        -  404_NOT_FOUND: if the request is not successful
        -  403_FORBIDDEN: if the request is not successful
        -  202_ACCEPTED: if the request is successful
    '''

    def put(self, request, pk):
        # Admin can update any user
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Admin can modify any user.
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    This method is used to partial update the user

    Accepts:
        pk (int): primary key of the user
        request data : JSON objects containing the data of the user to be updated
    Returns:
        -  200_OK: if the request is successful
        -  404_NOT_FOUND: if the request is not successful
        -  400_BAD_REQUEST: if the request is not successful
        -  403_FORBIDDEN: if the request is not successful
    '''
    
    def patch(self, request, pk):
        # Admin can patch any user; user can patch their own data
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If the user is not an admin, check if they are trying to modify themselves
        if user != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to modify this user."}, status=status.HTTP_403_FORBIDDEN)
        
        # If the user is modifying their own data, prevent them from deactivating themselves or changing the role
        if user == request.user:
            # if request.data['is_active'] is False:
            #     # Block non-admin users from deactivating their own account
            #     return Response({"detail": "You cannot deactivate your own account but you delete the account."}, status=status.HTTP_400_BAD_REQUEST)
            if 'is_active' in request.data and request.data['is_active'] is False:
                # Block non-admin users from deactivating their own account
                return Response({"detail": "You cannot deactivate your own account but you delete the account."}, status=status.HTTP_400_BAD_REQUEST)
            if 'role' in request.data:
                # Block non-admin users from changing the role field
                return Response({"detail": "You cannot modify the 'role' field."}, status=status.HTTP_400_BAD_REQUEST)

        # If the user is an admin, allow them to modify any user, including the 'role' field
        if 'role' in request.data and not request.user.is_staff:
            # Users cannot modify the role field
            return Response({"detail": "You cannot modify the 'role' field."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    '''
    This method is used to delete the user
    Accepts:
        pk (int): primary key of the user
    
    Returns:
        -  204_NO_CONTENT: if the request is successful
        -  404_NOT_FOUND: if the request is not successful
        -  403_FORBIDDEN: if the request is not successful
    '''


    def delete(self, request, pk):
        # Admin can delete any user; users can deactivate themselves
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
 
        if user != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to delete this user."}, status=status.HTTP_403_FORBIDDEN)
 
        # If a user wants to delete their account, set `is_active` to False
        if user == request.user:
            user.is_active = False
            if hasattr(user, 'profile'):  #  the user has a related Profile model
                user.profile.is_active = False
                user.profile.save()

            if hasattr(user, 'preferences'):  #  the user has a related Preferences model
                user.preferences.is_active = False
                user.preferences.save()


            user.save()
            return Response({"detail": "Your account has been deactivated."}, status=status.HTTP_200_OK)
 
        # Admins can delete any user
        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

'''
This PasswordUpdateView is used to update the password of a user

'''

class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    '''
    This method is used to update the password of a user
    Accepts:
        request data : JSON objects containing the data of the user to be updated
    
    Returns:
        -  200_OK: if the request is successful
        -  400_BAD_REQUEST: if the request is not successful

    '''

    def post(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.password_updated_at = timezone.now()
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ActiveUser(APIView):
    '''
    This view handles requests to retrieve Users based on their active status.

    Accepted :
        - GET: API request to Retrieve active or inactive users or a specific user by username.
        - active (str): A string that indicates the desired user status:
            - "active": Fetch all active users.
            - "inactive": Fetch all inactive users.
        - username (optional): str (The username of the specific user to retrieve)
    Responses:
        - 200 OK: Returns a list of active/inactive 
        - 404 Not Found: If a specific user is requested but does not exist or is inactive.
        - 400 Bad Request: If the 'active' parameter is invalid.
    '''
    def get(self, request, active, username=None):
        if username is not None:
            try:
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'Detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if active == 'active':
            users = User.objects.filter(is_active=True)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        elif active == 'inactive':
            users = User.objects.filter(is_active=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response({'Detail': 'Invalid active parameter'}, status=status.HTTP_400_BAD_REQUEST)  
    
'''
This is the UserCountView class which is used to get the count of active, inactive, and total users
'''
class UserCountView(APIView):

    '''
    This method retrieves the count of active, inactive, and total users.

    Accepted :
        - GET: API request to Retrieve the count of active, inactive, and total users.

    Responses:
        - 200 OK: Returns a dictionary containing the count of active, inactive, and total users.
    '''
    def get(self, request):
        total_count = User.objects.aggregate(
                                                  total_users=Count('username'),
                                                  active_users=Count('username',filter=Q(is_active=True)),
                                                  inactive_users=Count('username',filter=Q(is_active=False)),
                                                  )

        return Response(total_count, status=status.HTTP_200_OK)

'''
These AdminTokenView is used to get the token of a user
'''    

class AdminTokenView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    These method is used to get the token of a user
    Accepts:
        request data : JSON objects containing the username and password of a user
    Returns:
        -  200_OK: if the request user is found and the token is generated
        -  404_NOT_FOUND: if the request user is not found
        -  403_FORBIDDEN: if the user is not an admin
    '''

    def get(self, request):
        if request.user.role.role != 'Admin':
            return Response({'Detail':'You do not have permission to view this token'}, status=status.HTTP_403_FORBIDDEN)
        
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'username': username,'token': token.key}, status=status.HTTP_200_OK)
    
        except User.DoesNotExist:
            return Response({'Detail':'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
'''
These SearchView is used to search the user based on the search query
'''


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    """
        Handle user search request with multiple validation checks
        
        Query Parameters:
        - q: Search query string
        
        Returns:
        - Paginated list of matching users
    """

    def get(self, request):
        # Check if user is staff
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # Check if user is active
        if not request.user.is_active:
            return Response({"detail": "Inactive user"}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve search query from query parameters
        search_query = request.GET.get('q', '').strip()
        
        # Validate search query
        if not search_query:
            return Response({'error': 'Search query cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Query the User model fields directly (no need for profile__ prefix)
        users = User.objects.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |  
            Q(username__icontains=search_query) |  
            Q(email__icontains=search_query) |  
            Q(phone_number__icontains=search_query) | 
            Q(gender__gender__icontains=search_query) 
        )

        # Handle pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Customize the page size as needed

        # Paginate the queryset
        result_page = paginator.paginate_queryset(users, request)
        
        # Serialize the paginated data
        serializer = UserSerializer(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)