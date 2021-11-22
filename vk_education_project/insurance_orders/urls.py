from django.urls import path

from .views import list_offers, offer_details, create_offer, update_offer, delete_offer
from .views import list_zones, zone_details, create_zone, update_zone, delete_zone
from .views import list_options, option_details, create_option, update_option, delete_option

from .views import OptionDetailsView, OrderDetailsView, ZoneDetailsView
from .views import OptionCreateView, OrderCreateView, ZoneCreateView
from .views import OptionListView, OrderListView, ZonesListView


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

    path('api/v2/create', OrderCreateView.as_view(), name='Create offer with REST Framework'),
    path('api/v2/list', OrderListView.as_view(), name='Offer list with REST Framework'),
    path('api/v2/<int:pk>/details', OrderDetailsView.as_view(), name='Offer details with REST Framework'),

    path('zones/api/v2/create', ZoneCreateView.as_view(), name='Create offer with REST Framework'),
    path('zones/api/v2/list', ZonesListView.as_view(), name='Offer list with REST Framework'),
    path('zones/api/v2/<int:pk>/details', ZoneDetailsView.as_view(), name='Offer details with REST Framework'),

    path('options/api/v2/create', OptionCreateView.as_view(), name='Create offer with REST Framework'),
    path('options/api/v2/list', OptionListView.as_view(), name='Offer list with REST Framework'),
    path('options/api/v2/<int:pk>/details', OptionDetailsView.as_view(), name='Offer details with REST Framework'),

]
