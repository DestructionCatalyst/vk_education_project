from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods
from rest_framework import generics
from django.db.utils import IntegrityError
from django.http import JsonResponse, QueryDict

from .models import InsuranceOrders, Zones, InsuranceOptions
from insurance_companies.models import InsuranceCompanies
from api_views import api_function_of, details_api_function_of
from api_views import list_objects, object_details, create_object, update_object, delete_object
from .serializers import OrdersListSerializer, OrderDetailSerializer, OptionListSerializer, OptionDetailSerializer, \
    ZonesListSerializer, ZoneDetailSerializer


offer_api_function = api_function_of(InsuranceOrders)
offer_details_api_function = details_api_function_of(InsuranceOrders)

list_offers = offer_api_function(list_objects)
offer_details = offer_details_api_function(object_details)


@require_POST
def create_offer(request):
    try:
        params = request.POST.dict()
        params['zone'] = Zones.objects.get(pk=params['zone'])
        params['company'] = InsuranceCompanies.objects.get(pk=params['company'])
        available_options = params.pop('available_options')
        available_options = set(map(lambda option_id: InsuranceOptions.objects.get(pk=int(option_id.strip())),
                                    available_options.strip('[]').split(',')))
        new_offer = InsuranceOrders(**params)
        new_offer.save()
        new_offer.available_options.set(available_options)
        return JsonResponse(new_offer.as_dict(), status=201)
    except TypeError as e:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['PUT'])
def update_offer(request, object_id):
    params = QueryDict(request.body).dict()
    try:
        if InsuranceOrders.objects.filter(pk=object_id).exists():
            status = 200
        else:
            status = 201
        params['zone'] = Zones.objects.get(pk=params['zone'])
        params['company'] = InsuranceCompanies.objects.get(pk=params['company'])
        available_options = params.pop('available_options')
        available_options = set(map(lambda option_id: InsuranceOptions.objects.get(pk=int(option_id.strip())),
                                    available_options.strip('[]').split(',')))
        new_offer = InsuranceOrders(pk=object_id, **params)
        new_offer.save()
        new_offer.available_options.set(available_options)
        return JsonResponse(new_offer.as_dict(), status=status)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except TypeError as e:
        print(e)
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


delete_offer = offer_details_api_function(delete_object)

zone_api_function = api_function_of(Zones)
zone_details_api_function = details_api_function_of(Zones)

list_zones = zone_api_function(list_objects)
zone_details = zone_details_api_function(object_details)
create_zone = zone_api_function(create_object)
update_zone = zone_details_api_function(update_object)
delete_zone = zone_details_api_function(delete_object)


option_api_function = api_function_of(InsuranceOptions)
option_details_api_function = details_api_function_of(InsuranceOptions)

list_options = option_api_function(list_objects)
option_details = option_details_api_function(object_details)
create_option = option_api_function(create_object)
update_option = option_details_api_function(update_object)
delete_option = option_details_api_function(delete_object)


class ZoneCreateView(generics.CreateAPIView):
    serializer_class = ZoneDetailSerializer


class ZonesListView(generics.ListAPIView):
    serializer_class = ZonesListSerializer
    queryset = Zones.objects.all()


class ZoneDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ZoneDetailSerializer
    queryset = Zones.objects.all()


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer


class OrderListView(generics.ListAPIView):
    serializer_class = OrdersListSerializer
    queryset = InsuranceOrders.objects.all()


class OrderDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderDetailSerializer
    queryset = InsuranceOrders.objects.all()


class OptionCreateView(generics.CreateAPIView):
    serializer_class = OptionDetailSerializer


class OptionListView(generics.ListAPIView):
    serializer_class = OptionListSerializer
    queryset = InsuranceOptions.objects.all()


class OptionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OptionDetailSerializer
    queryset = InsuranceOptions.objects.all()
