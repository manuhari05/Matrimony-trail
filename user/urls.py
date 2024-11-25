# these are rest_framework imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

# these are django imports
from django.urls import path

# these are local imports
from .views import UserListCreateView, UserDetailUpdateDeleteView, PasswordUpdateView, AdminTokenView
from .views import ActiveUser, UserCountView, LoginView, SearchView


urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailUpdateDeleteView.as_view(), name='user-detail-update-delete'),
    path('update-password/', PasswordUpdateView.as_view(), name='password-update'),

    path('get-token/',obtain_auth_token,name='get-token'),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('admin-token/', AdminTokenView.as_view(), name='admin-token'),

    path('active/<str:active>/', ActiveUser.as_view(), name='active_student'),
    path('active/<str:active>/<str:username>/', ActiveUser.as_view(), name='active_student'),
    path('count/', UserCountView.as_view(), name='student_count'),

    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchView.as_view(), name='search'),

    
]