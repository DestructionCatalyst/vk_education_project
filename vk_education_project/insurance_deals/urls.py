from django.urls import path

from .views import list_deals, deal_details, create_deal, update_deal, delete_deal
from .views import DealDetailsView, DealCreateView, DealsListView


urlpatterns = [
    path('api/v1/list', list_deals, name='Deals list'),
    path('api/v1/<int:object_id>/details', deal_details, name='Deal details'),
    path('api/v1/create', create_deal, name='Create deal'),
    path('api/v1/<int:object_id>/update', update_deal, name='Update deal'),
    path('api/v1/<int:object_id>/delete', delete_deal, name='Delete deal'),

    path('api/v2/create', DealCreateView.as_view(), name='Create deal with REST Framework'),
    path('api/v2/list', DealsListView.as_view(), name='Deals list with REST Framework'),
    path('api/v2/<int:pk>/details', DealDetailsView.as_view(), name='Deal details with REST Framework'),
]
