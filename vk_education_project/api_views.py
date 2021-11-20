from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import ForeignKey
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse, QueryDict


def api_function_of(model_type):
    def api_function_decorator(func):
        def api_function_wrapped(request):
            return func(request, model_type)
        return api_function_wrapped
    return api_function_decorator


def details_api_function_of(model_type):
    def api_function_decorator(func):
        def api_function_wrapped(request, object_id):
            return func(request, object_id, model_type)
        return api_function_wrapped
    return api_function_decorator


@require_GET
def list_objects(request, model_type):
    objects_list = model_type.objects.all()
    objects_dicts = [obj.as_dict() for obj in objects_list]
    return JsonResponse({'data': objects_dicts})


@require_GET
def object_details(request, object_id, model_type):
    try:
        obj = model_type.objects.get(pk=object_id)
        return JsonResponse({'company': obj.as_dict()})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@require_POST
def create_object(request, model_type):
    try:
        new_object = model_type(**request.POST.dict())
        new_object.save()
        return JsonResponse(new_object.as_dict(), status=201)
    except TypeError:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['PUT'])
def update_object(request, object_id, model_type):
    params = QueryDict(request.body).dict()
    try:
        if model_type.objects.filter(pk=object_id).exists():
            status = 200
        else:
            status = 201
        obj = model_type(pk=object_id, **params)
        obj.save()
        return JsonResponse(obj.as_dict(), status=status)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except TypeError:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['DELETE'])
def delete_object(request, object_id, model_type):
    try:
        obj = model_type.objects.get(pk=object_id)
        obj.delete()
        return JsonResponse({'data': obj.as_dict()})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)
