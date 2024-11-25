from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound

from .models import Role, Gender, Subscription, GeneralTable
from .serializers import RoleSerializer, GenderSerializer, SubscriptionSerializer, GeneralTableSerializer
from .models import HelpRequest
from .serializers import HelpRequestSerializer
from notification.models import Notification
from user.models import User

genders = Gender.objects.all()

# Create your views here.

'''
These views are used to handle the CRUD operations for the Role, Gender, Subscription, and GeneralTable models.
They use the RoleSerializer, GenderSerializer, SubscriptionSerializer, and GeneralTableSerializer to serialize and deserialize the data.
The views are accessed using the APIView class and the appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE).
The views are protected by the IsAuthenticated permission class, which ensures that only authenticated users can access the views.
'''
class RoleView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, code=None):
        if code is not None:
            try:
                role = Role.objects.get(code=code)
                serializer = RoleSerializer(role)
                return Response(serializer.data)
            except Role.DoesNotExist:
                return Response({"error":"Role is not found"},status=status.HTTP_404_NOT_FOUND)
        
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, code):
        try:
            role = Role.objects.get(code=code)
        except Role.DoesNotExist:
            return Response({"error":"Role is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, code):
        try:
            role = Role.objects.get(code=code)
        except Role.DoesNotExist:
            return Response({"error":"Role is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, code):
        try:
            role = Role.objects.get(code=code)
        except Role.DoesNotExist:
            return Response({"error":"Role is not found"}, status=status.HTTP_404_NOT_FOUND)

        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GenderView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, code=None):
        if code is not None:
            try:
                gender = Gender.objects.get(code=code)
                serializer = GenderSerializer(gender)
                return Response(serializer.data)
            except Gender.DoesNotExist:
                return Response({"error":"Gender is not found"}, status=status.HTTP_404_NOT_FOUND)
            
        gender = Gender.objects.all()
        serializer = GenderSerializer(gender, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, code):
        try:
            gender = Gender.objects.get(code=code)
        except Gender.DoesNotExist:
            return Response({"error":"Gender is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenderSerializer(gender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, code):
        try:
            gender = Gender.objects.get(code=code)
        except Gender.DoesNotExist:
            return Response({"error":"Gender is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenderSerializer(gender, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, code):
        try:
            gender = Gender.objects.get(code=code)
        except Gender.DoesNotExist:
            return Response({"error":"Gender is not found"}, status=status.HTTP_404_NOT_FOUND)

        gender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SubscriptionView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, code=None):
        if code is not None:
            try:
                subscription = Subscription.objects.get(code=code)
                serializer = SubscriptionSerializer(subscription)
                return Response(serializer.data)
            except Subscription.DoesNotExist:
                return Response({"error":"Subscription is not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, code):
        try:
            subscription = Subscription.objects.get(code=code)
        except Subscription.DoesNotExist:
            return Response({"error":"Subscription is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, code):
        try:
            subscription = Subscription.objects.get(code=code)
        except Subscription.DoesNotExist:
            return Response({"error":"Subscription is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, code):
        try:
            subscription = Subscription.objects.get(code=code)
        except Subscription.DoesNotExist:
            return Response({"error":"Subscription is not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class HelpRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        This view allows the authenticated user to create a help request.
        """
        if request.user.is_staff:
            return Response({"error": "Admins are not allowed to create help requests."}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        subject = request.data.get("subject")
        description = request.data.get("description")

        if not subject or not description:
            return Response({"error": "Subject and Description are required."}, status=status.HTTP_400_BAD_REQUEST)

        help_request = HelpRequest.objects.create(
            user=user,
            subject=subject,
            description=description
        )
        
        # Notify Admin
        admin_users = User.objects.filter(is_superuser=True)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=f"New Help Request from {user.username} - {subject}"
            )

        return Response(HelpRequestSerializer(help_request).data, status=status.HTTP_201_CREATED)


class HelpRequestAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Admin can view all help requests.
        
        """
        if not request.user.is_superuser:
            return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_403_FORBIDDEN)
        help_requests = HelpRequest.objects.all()
        serializer = HelpRequestSerializer(help_requests, many=True)
        return Response(serializer.data)

    def patch(self, request, help_request_id):
        """
        Admin can update the status of the help request (e.g., mark as 'in progress' or 'closed').
        """
        if not request.user.is_superuser:
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        try:
            help_request = HelpRequest.objects.get(id=help_request_id)
        except HelpRequest.DoesNotExist:
            return Response({"error": "Help Request not found."}, status=status.HTTP_404_NOT_FOUND)

        status = request.data.get('status')
        if status not in ['open', 'in_progress', 'closed']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        help_request.status = status
        help_request.save()

        # Notify the user
        Notification.objects.create(
            user=help_request.user,
            message=f"Your Help Request has been updated to '{status}' status."
        )

        return Response(HelpRequestSerializer(help_request).data)

    
class GeneralTableView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, code=None):
        if code is not None:
            code = code.upper() # Ensure code is uppercase

            # Query for records that start with the provided code
            general_table = GeneralTable.objects.filter(code__startswith=code)

           
            if general_table.exists():
                serializer = GeneralTableSerializer(general_table, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "No records found with the provided code prefix."}, status=status.HTTP_404_NOT_FOUND)

        # If no code is provided, return all GeneralTable records
        general_table = GeneralTable.objects.all()
        serializer = GeneralTableSerializer(general_table, many=True)
        return Response(serializer.data)
    
class GeneralTableListCreate(ListCreateAPIView):
    queryset = GeneralTable.objects.all()  
    serializer_class = GeneralTableSerializer
    permission_classes = [IsAuthenticated]

class GeneralTableDetail(RetrieveUpdateDestroyAPIView):
    queryset = GeneralTable.objects.all()
    serializer_class = GeneralTableSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override this method to retrieve an object by its 'code' field, not by 'id'.
        """
        code = self.kwargs.get('code')  # Extract the 'code' from the URL
        try:
            obj = GeneralTable.objects.get(code=code)
        except GeneralTable.DoesNotExist:
            raise NotFound(detail="Not found", code=404)
        return obj