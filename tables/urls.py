# these are the django imports
from django.urls import path

# these are the local imports
from .views import RoleView, GenderView, SubscriptionView, GeneralTableListCreate, GeneralTableDetail
from .views import GeneralTableView, HelpRequestCreateView, HelpRequestAdminView

urlpatterns = [
    path('role/', RoleView.as_view(), name='role'),
    path('role/<str:code>/', RoleView.as_view(), name='role'),

    path('gender/', GenderView.as_view(), name='gender'),
    path('gender/<str:code>/', GenderView.as_view(), name='gender'),

    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('subscription/<str:code>/', SubscriptionView.as_view(), name='subscription'),

    path('general/', GeneralTableListCreate.as_view(), name='general'),
    path('general/<str:code>/', GeneralTableDetail.as_view(), name='general'),

    path('general-table/', GeneralTableView.as_view(), name='general-table'),
    path('general-table/<str:code>/', GeneralTableView.as_view(), name='general-table'),

    path('help/request/', HelpRequestCreateView.as_view(), name='help_request_create'),  
    path('help/admin/', HelpRequestAdminView.as_view(), name='help_request_admin'),  
    path('help/admin/<int:help_request_id>/', HelpRequestAdminView.as_view(), name='help_request_admin_detail'),  


]