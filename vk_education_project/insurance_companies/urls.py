from django.urls import path
from .views import index, list_companies, company_details, create_company, update_company, delete_company
from .views import CompanyCreateView, CompaniesListView, CompanyDetailsView

urlpatterns = [
    path('', index, name='Companies list'),
    path('api/v1/list', list_companies, name='JSON companies list'),
    path('api/v1/<int:company_id>/details', company_details, name='Company details'),
    path('api/v1/create', create_company, name='Create company'),
    path('api/v1/<int:company_id>/update', update_company, name='Update company'),
    path('api/v1/<int:company_id>/delete', delete_company, name='Delete company'),

    path('api/v2/create', CompanyCreateView.as_view(), name='Create company with REST Framework'),
    path('api/v2/list', CompaniesListView.as_view(), name='Companies list with REST Framework'),
    path('api/v2/<int:pk>/details', CompanyDetailsView.as_view(), name='Company details with REST Framework'),
]
