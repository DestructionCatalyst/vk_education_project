from django.db import models


class InsuranceCompanies(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    bank_details = models.JSONField()
    address = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страховая компания'
        verbose_name_plural = 'Страховые компании'
        ordering = ['-name']
