from django.urls import path

from .views import index, list_users, user_details, create_user, update_user, delete_user
from .views import UserDetailsView, UserCreateView, UsersListView
from .views import login_user, register_user, logout_user


urlpatterns = [
    path('', index, name='index'),

    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),

    path('api/v1/list', list_users, name='Users list'),
    path('api/v1/<int:object_id>/details', user_details, name='User details'),
    path('api/v1/create', create_user, name='Create user'),
    path('api/v1/<int:object_id>/update', update_user, name='Update user'),
    path('api/v1/<int:object_id>/delete', delete_user, name='Delete user'),

    path('api/v2/create', UserCreateView.as_view(), name='Create user with REST Framework'),
    path('api/v2/list', UsersListView.as_view(), name='Users list with REST Framework'),
    path('api/v2/<int:pk>/details', UserDetailsView.as_view(), name='User details with REST Framework'),
]
