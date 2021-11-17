from rest_framework import serializers
from .models import InsuranceCompanies


class CompaniesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompanies
        fields = ('id', 'name', 'website')


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompanies
        fields = '__all__'
