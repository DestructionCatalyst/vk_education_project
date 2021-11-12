from django.contrib import admin

from .models import InsuranceUsers, InsuranceDeals

admin.site.register(InsuranceUsers)
admin.site.register(InsuranceDeals)

