from django.urls import path

from .views import index, list_users, user_details, create_user, update_user, delete_user
from .views import list_deals, deal_details, create_deal, update_deal, delete_deal

from .views import UserDetailsView, UserCreateView, UsersListView
from .views import DealDetailsView, DealCreateView, DealsListView


urlpatterns = [
    path('', index),

    path('api/v1/list', list_users, name='Users list'),
    path('api/v1/<int:object_id>/details', user_details, name='User details'),
    path('api/v1/create', create_user, name='Create user'),
    path('api/v1/<int:object_id>/update', update_user, name='Update user'),
    path('api/v1/<int:object_id>/delete', delete_user, name='Delete user'),

    path('deals/api/v1/list', list_deals, name='Deals list'),
    path('deals/api/v1/<int:object_id>/details', deal_details, name='Deal details'),
    path('deals/api/v1/create', create_deal, name='Create deal'),
    path('deals/api/v1/<int:object_id>/update', update_deal, name='Update deal'),
    path('deals/api/v1/<int:object_id>/delete', delete_deal, name='Delete user'),

    path('api/v2/create', UserCreateView.as_view(), name='Create user with REST Framework'),
    path('api/v2/list', UsersListView.as_view(), name='Users list with REST Framework'),
    path('api/v2/<int:pk>/details', UserDetailsView.as_view(), name='User details with REST Framework'),

    path('deals/api/v2/create', DealCreateView.as_view(), name='Create deal with REST Framework'),
    path('deals/api/v2/list', DealsListView.as_view(), name='Deals list with REST Framework'),
    path('deals/api/v2/<int:pk>/details', DealDetailsView.as_view(), name='Deal details with REST Framework'),
]
