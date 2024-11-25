# these are django imports
from django.urls import path

# these are the local imports
from .views import NotificationAdminView, NotificationView


urlpatterns = [
    path('admin/', NotificationAdminView.as_view(), name='notifications'),

    path('user', NotificationView.as_view(), name='notifications')
    
]