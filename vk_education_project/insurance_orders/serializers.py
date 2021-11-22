from rest_framework import serializers
from .models import InsuranceOrders, InsuranceOptions, Zones


class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceOrders
        fields = ('id', 'zone', 'company')


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceOrders
        fields = '__all__'


class ZonesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zones
        fields = ('id', 'name')


class ZoneDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zones
        fields = '__all__'


class OptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceOptions
        fields = ('id', 'name')


class OptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceOptions
        fields = '__all__'

