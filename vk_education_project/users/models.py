from django.db import models
from django.contrib.auth.models import AbstractUser


class InsuranceUsers(AbstractUser):
    first_name = models.CharField(blank=False, max_length=150, verbose_name='Имя')
    last_name = models.CharField(blank=False, max_length=150, verbose_name='Фамилия')
    email = models.EmailField(blank=False, verbose_name='Адрес электронной почты')
    document_number = models.CharField(max_length=10, blank=True,
                                       verbose_name='Номер документа, удостоверяющего личность')
    phone = models.CharField(max_length=16, blank=True, verbose_name='Номер телефона')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения')

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def as_dict(self):
        return {'id': self.pk,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'document_number': self.document_number,
                'phone': self.phone,
                'birth_date': self.birth_date,
                }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-last_name']



