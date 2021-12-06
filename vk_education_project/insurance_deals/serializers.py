from .models import InsuranceDeals
from rest_framework import serializers


class DealsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceDeals
        fields = ('id', 'holder', 'order')


class DealDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceDeals
        fields = '__all__'
