from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from .serializers import NotificationSerializer
from .models import Notification
# Create your views here.

'''
These NotificationAdminView is used to get the list of all notifications 
'''

class NotificationAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            notifications = Notification.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(notifications, request)
            serializer = NotificationSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        else:
            return Response({"error":"You are not authorized to view this page"},status=status.HTTP_403_FORBIDDEN)
        
'''
These NotificationView is used to get the list of all notifications and mark them as read
'''
class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    '''
    These method is used to get the list of all notifications of the user
    Accepts:
        Authentications: user must be authenticated for user
    Returns:
        - 200 OK: List of notifications of the user
        - 403 Forbidden: If the user is not authenticated
    
    '''

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    '''
    These method is used to mark all notifications as read
    Accepts:
        Authentications: user must be authenticated for user
    returns:
        - 200 OK: If all notifications are marked as read
        - 400 Bad Request: If there are no unread notifications to mark as read
        - 403 Forbidden: If the user is not authenticated
    '''
    
    def patch(self, request):
        notifications = Notification.objects.filter(user=request.user)
        if notifications.exists():
            notifications.update(is_read=True)
            return Response({"message": "All notifications marked as read."}, status=status.HTTP_200_OK)
        
        return Response({"message": "No unread notifications to mark as read."}, status=status.HTTP_200_OK)
    # def post(self, request):
    #     serializer = NotificationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request):
    #     notifications = Notification.objects.filter(user=request.user)
    #     notifications.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)