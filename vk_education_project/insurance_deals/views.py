from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods, require_GET
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

from .tasks import send_created_deal_mail
import json

deal_api_function = api_function_of(InsuranceDeals)
deal_details_api_function = details_api_function_of(InsuranceDeals)

user_required = login_required()
admin_required = login_required(need_admin=True)

@user_required
@require_GET
def list_deals(request):
    deal_list = InsuranceDeals.objects.filter(holder_id=request.user.id)
    deal_dicts = [obj.as_dict() for obj in deal_list]
    return JsonResponse({'data': deal_dicts})


@login_required
@require_GET
def deal_details(request, object_id):
    try:
        deal = InsuranceDeals.objects.get(pk=object_id)
        if deal['holder'] == request.user.id or request.user.is_staff:
            return JsonResponse({'data': deal.as_dict()})
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@login_required
@require_POST
def create_deal(request):
    try:
        params = request.POST.dict()
        if params['holder'] == request.user.id or request.user.is_staff:
            params['holder'] = InsuranceUsers.objects.get(pk=params['holder'])
            params['order'] = InsuranceOrders.objects.get(pk=params['order'])
            selected_options = params.pop('options')
            selected_options = set(map(lambda option_id: InsuranceOptions.objects.get(pk=int(option_id.strip())),
                                       selected_options.strip('[]').split(',')))
            new_offer = InsuranceDeals(**params)
            new_offer.save()
            new_offer.options.set(selected_options)
            message = f'Компания: {params["order"].company.name}\n' \
                      f'Зона действия: {params["order"].zone.name}\n' \
                      f'С {params["start_date"]} по {params["end_date"]}\n'
            for option in selected_options:
                message += f'{option.name}, страховая сумма {option.insurance_amount}$\n'
            send_created_deal_mail.delay(
                subject=f'Заключена страховка пользователем '
                        f'{request.user.username}({request.user.last_name} {request.user.first_name})',
                message=message
            )
            return JsonResponse(new_offer.as_dict(), status=201)
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)
    except TypeError as e:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(['PUT'])
def update_deal(request, object_id):
    params = QueryDict(request.body).dict()
    try:
        deal = InsuranceDeals.objects.get(pk=object_id)
        if deal.holder.id == request.user.id or request.user.is_staff:
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
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except TypeError as e:
        print(e)
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['DELETE'])
def delete_deal(request, object_id, model_type):
    try:
        deal = model_type.objects.get(pk=object_id)
        if deal['holder'] == request.user.id or request.user.is_staff:
            deal.delete()
            return JsonResponse({'data': deal.as_dict()})
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except ValueError:
        pass


class DealCreateView(generics.CreateAPIView, LoginRequiredMixin):
    serializer_class = DealDetailSerializer

    def create(self, request, *args, **kwargs):
        post_data = request.data
        if int(post_data['holder']) == request.user.id or request.user.is_staff:
            order = InsuranceOrders.objects.get(pk=post_data['order'])
            message = f'Компания: {order.company.name}\n' \
                      f'Зона действия: {order.zone.name}\n' \
                      f'С {post_data["start_date"]} по {post_data["end_date"]}\n'
            for option_id in request.POST.getlist('options'):
                option = InsuranceOptions.objects.get(pk=int(option_id))
                message += f'{option.name}, страховая сумма {option.insurance_amount}$\n'
            send_created_deal_mail.delay(
                subject=f'Заключена страховка пользователем '
                        f'{request.user.username}({request.user.last_name} {request.user.first_name})',
                message=message
            )
            return super(DealCreateView, self).create(request, args, kwargs)
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)


class DealsListView(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = DealsListSerializer
    queryset = InsuranceDeals.objects.all()

    def get_queryset(self):
        return InsuranceDeals.objects.filter(holder_id=self.request.user.id)


class DealDetailsView(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    serializer_class = DealDetailSerializer
    queryset = InsuranceDeals.objects.all()

    def get(self, request, *args, **kwargs):
        deal = InsuranceDeals.objects.get(pk=kwargs['pk'])
        if deal.holder.id == request.user.id or request.user.is_staff:
            return super(DealDetailsView, self).get(request, args, kwargs)
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)

    def put(self, request, *args, **kwargs):
        deal = InsuranceDeals.objects.get(pk=kwargs['pk'])
        if deal.holder.id == request.user.id or request.user.is_staff:
            return super(DealDetailsView, self).put(request, args, kwargs)
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)

    def patch(self, request, *args, **kwargs):
        deal = InsuranceDeals.objects.get(pk=kwargs['pk'])
        if deal.holder.id == request.user.id or request.user.is_staff:
            return super(DealDetailsView, self).patch(request, args, kwargs)
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)

    def delete(self, request, *args, **kwargs):
        deal = InsuranceDeals.objects.get(pk=kwargs['pk'])
        if deal.holder.id == request.user.id or request.user.is_staff:
            return super(DealDetailsView, self).delete(request, args, kwargs)
        else:
            return JsonResponse({'error': 'not enough permissions'}, status=403)
