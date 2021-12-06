from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods
from rest_framework import generics, status
from django.db.utils import IntegrityError
from django.http import JsonResponse, QueryDict

from api_views import api_function_of, details_api_function_of
from api_views import list_objects, object_details, create_object, update_object, delete_object
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import InsuranceUsers
from insurance_deals.models import InsuranceDeals
from .serializers import UsersListSerializer, UserDetailSerializer

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm
import os
from application.settings import TEMPLATE_DIR
from users.login_decorators import login_required


def index(request):
    deal = InsuranceDeals.objects.first()
    return JsonResponse({'test': deal.total_price()})

user_required = login_required()
admin_required = login_required(need_admin=True)


user_api_function = api_function_of(InsuranceUsers)
user_details_api_function = details_api_function_of(InsuranceUsers)

list_users = admin_required(user_api_function(list_objects))
user_details = admin_required(user_details_api_function(object_details))


@login_required(need_admin=True)
@require_POST
def create_user(request):
    try:
        params = request.POST.dict()
        new_user = InsuranceUsers.objects.create_user(params.get('username'),
                                                      params.get('email'),
                                                      params.get('password'))
        new_user.first_name = params.get('first_name')
        new_user.last_name = params.get('last_name')
        new_user.phone = params.get('phone')
        new_user.document_number = params.get('document_number')
        new_user.birth_date = params.get('birth_date')
        new_user.save()
        return JsonResponse({}, status=204)
    except TypeError as e:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


update_user = admin_required(user_details_api_function(update_object))


@login_required(need_admin=True)
@require_http_methods(['DELETE'])
def delete_user(request, object_id):
    try:
        user = InsuranceUsers.objects.get(pk=object_id)
        user.is_active = False
        user.save()
        return JsonResponse({'data': user.as_dict()})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except ValueError:
        pass


class UserCreateView(generics.CreateAPIView, UserPassesTestMixin):
    serializer_class = UserDetailSerializer

    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active


class UsersListView(generics.ListAPIView, UserPassesTestMixin):
    serializer_class = UsersListSerializer
    queryset = InsuranceUsers.objects.all()

    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView, UserPassesTestMixin):
    serializer_class = UserDetailSerializer
    queryset = InsuranceUsers.objects.all()

    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.user.is_authenticated:
        return redirect('Companies list')
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Companies list')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    else:
        form = UserLoginForm()
        get
    return render(request, os.path.join(TEMPLATE_DIR, 'users/login_user.html'),
                  context={'title': 'Login user', 'form': form})


@require_http_methods(["GET", "POST"])
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            messages.success(request, "Успешная регистрация")
            return redirect('login')
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegistrationForm()
    return render(request, os.path.join(TEMPLATE_DIR, 'users/register_user.html'),
                  context={'title': 'Регистрация', 'form': form})


@require_http_methods(["GET", "POST"])
def logout_user(request):
    logout(request)
    return redirect('login')
