from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods
from rest_framework import generics, status
from django.db.utils import IntegrityError
from django.http import JsonResponse, QueryDict

from api_views import api_function_of, details_api_function_of
from api_views import list_objects, object_details, create_object, update_object, delete_object
from rest_framework.response import Response

from .models import InsuranceUsers
from insurance_orders.models import InsuranceOrders, InsuranceOptions
from .serializers import UsersListSerializer, UserDetailSerializer


def index(request):
    deal = InsuranceDeals.objects.first()
    return JsonResponse({'test': deal.total_price()})


user_api_function = api_function_of(InsuranceUsers)
user_details_api_function = details_api_function_of(InsuranceUsers)

list_users = user_api_function(list_objects)
user_details = user_details_api_function(object_details)


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


update_user = user_details_api_function(update_object)


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


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer


class UsersListView(generics.ListAPIView):
    serializer_class = UsersListSerializer
    queryset = InsuranceUsers.objects.all()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = InsuranceUsers.objects.all()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
