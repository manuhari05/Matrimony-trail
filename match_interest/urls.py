# these are django imports
from django.urls import path

# these are the local imports
from .views import MatchViewByAdmin, MatchViewBySubscription, MatchAPIView, MatchViewRequest, ViewMatchProfiles

urlpatterns = [
    path('admin',MatchViewByAdmin.as_view(),name='match-admin'),

    path('subscription', MatchViewBySubscription.as_view(), name='match-suscription'),

    path('match-interest',MatchAPIView.as_view(),name='match-interest'),
    path('match-interest/<int:match_id>', MatchAPIView.as_view(), name='match-interest'),

    path('match-request',MatchViewRequest.as_view(), name='match-request'),
    path('match-request/<int:match_id>', MatchViewRequest.as_view(), name='match-request'),

    path('match-profiles/<int:match_id>', ViewMatchProfiles.as_view(), name='match-profiles'),

]