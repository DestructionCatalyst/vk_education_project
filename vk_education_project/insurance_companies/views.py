from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from rest_framework import generics

import os
from application.settings import TEMPLATE_DIR
from .models import InsuranceCompanies
from .serializers import CompaniesListSerializer, CompanyDetailSerializer


@require_GET
def index(request):
    companies_list = InsuranceCompanies.objects.all()
    return render(request,
                  os.path.join(TEMPLATE_DIR, 'companies/index.html'),
                  {'title': 'Компании',
                   'companies': companies_list})


@require_GET
def list_companies(request):
    companies_list = InsuranceCompanies.objects.all()
    companies_dicts = [company.as_dict() for company in companies_list]
    return JsonResponse({'data': companies_dicts})


@require_GET
def company_details(request, company_id):
    try:
        company = InsuranceCompanies.objects.get(pk=company_id)
        return JsonResponse({'company': company.as_dict()})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@require_POST
def create_company(request):
    try:
        new_company = InsuranceCompanies(**request.POST.dict())
        new_company.save()
        return JsonResponse(new_company.as_dict(), status=201)
    except TypeError:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['PUT'])
def update_company(request, company_id):
    params = QueryDict(request.body).dict()
    try:
        if InsuranceCompanies.objects.filter(pk=company_id).exists():
            status = 200
        else:
            status = 201
        company = InsuranceCompanies(pk=company_id, **params)
        company.save()
        return JsonResponse(company.as_dict(), status=status)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except TypeError:
        return JsonResponse({'error': 'Unexpected parameters in request body'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['DELETE'])
def delete_company(request, company_id):
    try:
        company = InsuranceCompanies.objects.get(pk=company_id)
        company.delete()
        return JsonResponse({'company': company.as_dict()})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=500)


class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanyDetailSerializer


class CompaniesListView(generics.ListAPIView):
    serializer_class = CompaniesListSerializer
    queryset = InsuranceCompanies.objects.all()


class CompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyDetailSerializer
    queryset = InsuranceCompanies.objects.all()
