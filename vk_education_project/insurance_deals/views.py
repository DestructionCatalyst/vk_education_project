from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods
from rest_framework import generics
from django.db.utils import IntegrityError
from django.http import JsonResponse, QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin

from api_views import api_function_of, details_api_function_of
from api_views import list_objects, object_details, create_object, update_object, delete_object

from .models import InsuranceDeals
from users.models import InsuranceUsers
from insurance_orders.models import InsuranceOrders, InsuranceOptions
from .serializers import DealsListSerializer, DealDetailSerializer
from users.login_decorators import login_required

deal_api_function = api_function_of(InsuranceDeals)
deal_details_api_function = details_api_function_of(InsuranceDeals)

user_required = login_required()
admin_required = login_required(need_admin=True)

list_deals = user_required(deal_api_function(list_objects))
deal_details = user_required(deal_details_api_function(object_details))


@login_required
@require_POST
def create_deal(request):
    try:
        params = request.POST.dict()
        params['holder'] = InsuranceUsers.objects.get(pk=params['holder'])
        params['order'] = InsuranceOrders.objects.get(pk=params['order'])
        selected_options = params.pop('options')
        selected_options = set(map(lambda option_id: InsuranceOptions.objects.get(pk=int(option_id.strip())),
                                   selected_options.strip('[]').split(',')))
        new_offer = InsuranceDeals(**params)
        new_offer.save()
        new_offer.options.set(selected_options)
        return JsonResponse(new_offer.as_dict(), status=201)
    except TypeError as e:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(['PUT'])
def update_deal(request, object_id):
    params = QueryDict(request.body).dict()
    try:
        if InsuranceOrders.objects.filter(pk=object_id).exists():
            status = 200
        else:
            status = 201
        params['holder'] = InsuranceUsers.objects.get(pk=params['holder'])
        params['order'] = InsuranceOrders.objects.get(pk=params['order'])
        selected_options = params.pop('options')
        selected_options = set(map(lambda option_id: InsuranceOptions.objects.get(pk=int(option_id.strip())),
                                   selected_options.strip('[]').split(',')))
        new_offer = InsuranceDeals(**params)
        new_offer.save()
        new_offer.options.set(selected_options)
        return JsonResponse(new_offer.as_dict(), status=status)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except TypeError as e:
        print(e)
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


delete_deal = user_required(deal_details_api_function(delete_object))


class DealCreateView(generics.CreateAPIView, LoginRequiredMixin):
    serializer_class = DealDetailSerializer


class DealsListView(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = DealsListSerializer
    queryset = InsuranceDeals.objects.all()


class DealDetailsView(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    serializer_class = DealDetailSerializer
    queryset = InsuranceDeals.objects.all()

