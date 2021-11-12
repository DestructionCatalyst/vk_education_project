from django.contrib import admin

from .models import Zones, InsuranceOptions, InsuranceOrders

admin.site.register(Zones)
admin.site.register(InsuranceOptions)
admin.site.register(InsuranceOrders)
