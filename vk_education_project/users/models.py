from django.db import models
from django.contrib.auth.models import AbstractUser

from insurance_orders.models import InsuranceOptions
from insurance_orders.models import InsuranceOrders


class InsuranceUsers(AbstractUser):
    first_name = models.CharField(blank=False, max_length=150, verbose_name='Имя')
    last_name = models.CharField(blank=False, max_length=150, verbose_name='Фамилия')
    email = models.EmailField(blank=False, verbose_name='Адрес электронной почты')
    document_number = models.CharField(max_length=10, blank=True,
                                       verbose_name='Номер документа, удостоверяющего личность')
    phone = models.CharField(max_length=16, blank=True, verbose_name='Номер телефона')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения')

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-last_name']


class InsuranceDeals(models.Model):
    holder = models.ForeignKey(InsuranceUsers, on_delete=models.CASCADE, verbose_name='Владелец')
    order = models.ForeignKey(InsuranceOrders, on_delete=models.SET_NULL, null=True, verbose_name='Предложение')
    options = models.ManyToManyField(InsuranceOptions, verbose_name='Выбранные опции')
    start_date = models.DateField(verbose_name='Дата начала действия')
    end_date = models.DateField(verbose_name='Дата окончания действия')

    class Meta:
        verbose_name = 'Выбранное предложение'
        verbose_name_plural = 'Выбранные предложения'
