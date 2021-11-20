from django.urls import path
from .views import list_offers, offer_details, create_offer, update_offer, delete_offer
from .views import list_zones, zone_details, create_zone, update_zone, delete_zone
from .views import list_options, option_details, create_option, update_option, delete_option


urlpatterns = [
    path('api/v1/list', list_offers, name='Offers list'),
    path('api/v1/<int:object_id>/details', offer_details, name='Offer details'),
    path('api/v1/create', create_offer, name='Create offer'),
    path('api/v1/<int:object_id>/update', update_offer, name='Update offer'),
    path('api/v1/<int:object_id>/delete', delete_offer, name='Delete offer'),

    path('zones/api/v1/list', list_zones, name='Zones list'),
    path('zones/api/v1/<int:object_id>/details', zone_details, name='Zone details'),
    path('zones/api/v1/create', create_zone, name='Create zone'),
    path('zones/api/v1/<int:object_id>/update', update_zone, name='Update zone'),
    path('zones/api/v1/<int:object_id>/delete', delete_zone, name='Delete zone'),

    path('options/api/v1/list', list_options, name='Options list'),
    path('options/api/v1/<int:object_id>/details', option_details, name='Option details'),
    path('options/api/v1/create', create_option, name='Create option'),
    path('options/api/v1/<int:object_id>/update', update_option, name='Update option'),
    path('options/api/v1/<int:object_id>/delete', delete_option, name='Delete option'),
]
