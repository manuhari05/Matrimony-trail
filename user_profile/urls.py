# these are the django imports
from django.urls import path
from django.conf import settings

# these are the local imports
from .views import ProfileUpdateView, ProfileCreateView


urlpatterns = [
    # path('profile/', ProfileAPIView.as_view(), name='profile'),
    # path('profile/<int:pk>/', ProfileAPIView.as_view(), name='profile-detail')

    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    
    path('create-profile/', ProfileCreateView.as_view(), name='create-profile'),
    
    
] 