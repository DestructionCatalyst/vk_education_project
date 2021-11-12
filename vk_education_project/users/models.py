from django.db import models
from django.contrib.auth.models import AbstractUser

from insurance_orders.models import InsuranceOptions
from insurance_orders.models import InsuranceOrders


class InsuranceUsers(AbstractUser):
    first_name = models.CharField(blank=False, max_length=150)
    last_name = models.CharField(blank=False, max_length=150)
    email = models.EmailField(blank=False)
    document_number = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        ordering = ['-last_name']


class InsuranceDeals(models.Model):
    holder = models.ForeignKey(InsuranceUsers, on_delete=models.CASCADE)
    order = models.ForeignKey(InsuranceOrders, on_delete=models.SET_NULL, null=True)
    options = models.ManyToManyField(InsuranceOptions)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'Выбранное предложение'
        verbose_name_plural = 'Выбранные предложения'
