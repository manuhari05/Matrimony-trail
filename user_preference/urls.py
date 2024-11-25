#these are django imports
from django.urls import path
# these are local imports
from .views import PreferenceListCreateView, PreferenceUpdateView

urlpatterns = [
    path('preferences/', PreferenceListCreateView.as_view(), name='preference-create'),  
    
    path('preferences/update/', PreferenceUpdateView.as_view(), name='preference-update'),  
]
