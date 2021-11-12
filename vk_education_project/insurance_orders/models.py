from django.db import models

from insurance_companies.models import InsuranceCompanies


class Zones(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Таможенная зона'
        verbose_name_plural = 'Таможенные зоны'
        ordering = ['-name']


class InsuranceOptions(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    insurance_amount = models.DecimalField(max_digits=12, decimal_places=2)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    daily_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'
        ordering = ['-name']


class InsuranceOrders(models.Model):
    zone = models.ForeignKey(Zones, on_delete=models.CASCADE)
    company = models.ForeignKey(InsuranceCompanies, on_delete=models.CASCADE)
    available_options = models.ManyToManyField(InsuranceOptions)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    franchise = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Страховое предложение'
        verbose_name_plural = 'Страховые предложения'
