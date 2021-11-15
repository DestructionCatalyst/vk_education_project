from django.shortcuts import render
from django.http import JsonResponse
from .models import InsuranceDeals


def index(request):
    deal = InsuranceDeals.objects.first()
    return JsonResponse({'test': deal.total_price()})


