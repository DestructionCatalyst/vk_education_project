from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

from .models import InsuranceDeals, InsuranceUsers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password as builtin_validate_password


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceUsers
        fields = ('id', 'first_name', 'last_name', 'birth_date')


class UserDetailSerializer(serializers.ModelSerializer):
    email = EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=InsuranceUsers.objects.all())]
    )
    document_number = CharField(
        max_length=10,
        validators=[UniqueValidator(queryset=InsuranceUsers.objects.all())]
    )

    def validate_password(self, password):
        builtin_validate_password(password)
        return password

    def validate_phone(self, phone):
        if phone[0] != '+':
            raise serializers.ValidationError('Телефонные номера должны начинаться с "+"')
        try:
            int(phone)
            return phone
        except ValueError:
            raise serializers.ValidationError('Телефонные номера должны состоять только из цифр')

    class Meta:
        model = InsuranceUsers
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'document_number', 'phone', 'birth_date')
        extra_kwargs = {'password': {'write_only': True},
                        'document_number': {'write_only': True},
                        'birth_date': {'read_only': True}}


class DealsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceDeals
        fields = ('id', 'holder', 'order')


class DealDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceDeals
        fields = '__all__'

