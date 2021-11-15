from django.db import models

from insurance_companies.models import InsuranceCompanies


class Zones(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Таможенная зона'
        verbose_name_plural = 'Таможенные зоны'
        ordering = ['-name']


class InsuranceOptions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    insurance_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Страховая сумма')
    base_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Базовая цена')
    daily_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена за день пребывания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'
        ordering = ['-name']


class InsuranceOrders(models.Model):
    zone = models.ForeignKey(Zones, on_delete=models.CASCADE, verbose_name='Зона действия')
    company = models.ForeignKey(InsuranceCompanies, on_delete=models.PROTECT, verbose_name='Компания')
    available_options = models.ManyToManyField(InsuranceOptions, verbose_name='Доступные опции')
    min_age = models.IntegerField(verbose_name='Минимальный возраст')
    max_age = models.IntegerField(verbose_name='Максимальный возраст')
    franchise = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Франшиза')

    def __str__(self):
        return str(self.company) + ', ' + str(self.zone)

    class Meta:
        verbose_name = 'Страховое предложение'
        verbose_name_plural = 'Страховые предложения'
