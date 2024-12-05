from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination


from django.db.models import Sum ,Avg ,Count, Q


from .models import Message
from .serializers import MessageSerializer
from user.models import User
from notification.models import Notification
from match_interest.models import Match

# Create your views here.
'''
These MessageAdminView and MessageSendView are used to get the list of all messages and create a new message.
'''
class MessageAdminView(APIView):
    permission_classes = [IsAuthenticated]

    '''
    These mathod is used to get the list of all messages by the admin
    '''

    def get(self, request):
        if request.user.is_superuser:
            messages = Message.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(messages, request)
            serializer = MessageSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        else:
            return Response({"error":"You are not authorized to view this page"},status=status.HTTP_403_FORBIDDEN)



class MessageSendView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    These mathod is used to view the list of all messages sent by the user
    Accepts:
        Authentications: user must be authenticated for user1
    Returns:
        - 200 OK: List of messages sent by the user
        - 403 Forbidden: If the user is not authenticated
    '''

    def get(self, request):
        messages = Message.objects.filter(sender=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    '''
    These mathod is used to send a message to another user
    Accepts:
        Authentications: user must be authenticated for user1
        request data : user2 in the JSON data to send the message to
    Returns:
        - 201 Created: If the message is sent successfully
        - 400 Bad Request: If the request data is invalid
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the user2 does not exist
        - 400 Bad Request: If the user2 is the same as the authenticated user
        - 400 Bad Request: If the message content is empty or too long
    '''

    def post(self, request):
        # Superuser check
        if request.user.is_superuser:
            return Response({"error": "You are not authorized to send messages"}, status=status.HTTP_403_FORBIDDEN)
        
        user1 = request.user
        user2 = request.data.get('user2')  # assuming user2 is sent as part of the request data
        message_content = request.data.get('message')  # the message content

        # Validate that user2 exists
        try:
            user2_instance = User.objects.get(username=user2)
        except User.DoesNotExist:
            return Response({"error": f"User '{user2}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that sender is not the same as receiver
        if user1 == user2_instance:
            return Response({"error": "You cannot send a message to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate that the match exists and is accepted
        match_exists = Match.objects.filter(
            (Q(user1=user1) & Q(user2=user2_instance)) |
            (Q(user1=user2_instance) & Q(user2=user1))
        ).first()

        if not match_exists or match_exists.status != 'Accepted':
            return Response({"error": "No accepted match found between you and this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate message content (ensure it is not empty and within a reasonable length)
        if not message_content or len(message_content.strip()) == 0:
            return Response({"error": "Message content cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if len(message_content) > 1000:  # assuming you want a max length of 1000 characters
            return Response({"error": "Message content is too long. Maximum length is 1000 characters."}, status=status.HTTP_400_BAD_REQUEST)

       
        data = request.data.copy()  # Copy the request data to avoid modifying the original data
        data['receiver'] = user2_instance.pk  
        
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            Notification.objects.create(user=user2_instance,message = f"You have received a message from {user1.username}.")
            # Save the message with the authenticated user as the sender
            serializer.save(sender=user1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

      
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
'''
These MessageReceivedView is used to get the list of all messages received by the user and update the status of the message
'''

class MessageReceivedView(APIView):
    permission_classes = [IsAuthenticated]

    '''
    These method is used to get the list of all messages received by the user
    Accepts:
        Authentications: user must be authenticated for user2
    Returns:
        - 200 OK: List of messages received by the user
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the user is not found
        - 400 Bad Request: If the user is not active
    '''

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    '''
    These method is used to update the status of the message
    Accepts:
        Authentications: user must be authenticated for user2
        message_id: id of the message to be updated
    Returns:
        - 200 OK: If the message is updated successfully
        - 400 Bad Request: If the request data is invalid
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the message does not exist
    '''
    
    def patch(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, receiver=request.user)
        except Message.DoesNotExist:
            return Response({"error": "Message not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

        message.is_read = True
        Notification.objects.create(user = message.sender, message = f"Your message has been read by {request.user.username}.")
        message.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)
    

class MessageOfUserView(APIView):
    permission_classes = [IsAuthenticated]

    '''
    These method is used to get the list of all messages between the user and the other user
    Accepts:
        Authentications: user must be authenticated for user1
        user2: username of the other user
    Returns:
        - 200 OK: List of messages between the user and the other user
        - 403 Forbidden: If the user is not authenticated
        - 404 Not Found: If the user2 does not exist
        - 400 Bad Request: If the user2 is the same as the authenticated user
    '''

    def get(self, request, user2):
        user1 = request.user
        user2 = User.objects.get(username=user2)

        if user1 == user2:
            return Response({"error": "You cannot send a message to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        messages = Message.objects.filter(
            (Q(sender=user1) & Q(receiver=user2)) | (Q(sender=user2) & Q(receiver=user1))
        ).order_by('timestamp')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
