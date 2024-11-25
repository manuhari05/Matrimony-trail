# these are django imports
from django.urls import path

# these are local imports
from .views import MessageAdminView, MessageSendView, MessageReceivedView


urlpatterns = [
    path('admin',MessageAdminView.as_view(),name='message-admin'),
    path('send', MessageSendView.as_view(), name='message-send'),
    path('received', MessageReceivedView.as_view(), name='message-received'),
    path('received/<int:message_id>', MessageReceivedView.as_view(), name='message-received-detail'),

]