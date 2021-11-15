from django.db import models


class InsuranceCompanies(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    phone = models.CharField(max_length=16, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Адрес электронной почты')
    website = models.CharField(max_length=255, verbose_name='Сайт')
    bank_details = models.JSONField(verbose_name='Банковские реквизиты')
    address = models.CharField(max_length=512, verbose_name='Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страховая компания'
        verbose_name_plural = 'Страховые компании'
        ordering = ['-name']
