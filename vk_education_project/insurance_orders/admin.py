from django.contrib import admin

from .models import Zones, InsuranceOptions, InsuranceOrders

admin.site.register(Zones)


@admin.register(InsuranceOptions)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'insurance_amount')


admin.site.register(InsuranceOrders)
