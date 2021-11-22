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


class InsuranceDeals(models.Model):
    holder = models.ForeignKey(InsuranceUsers, on_delete=models.CASCADE, verbose_name='Владелец')
    order = models.ForeignKey(InsuranceOrders, on_delete=models.SET_NULL, null=True, verbose_name='Предложение')
    options = models.ManyToManyField(InsuranceOptions, verbose_name='Выбранные опции')
    start_date = models.DateField(verbose_name='Дата начала действия')
    end_date = models.DateField(verbose_name='Дата окончания действия')

    def __str__(self):
        return str(self.holder) + ', ' + str(self.order)

    def as_dict(self):
        return {'id': self.pk,
                'holder': self.holder.as_dict(),
                'order': self.order.as_dict(),
                'options': list(map(lambda option: option.as_dict(), self.options.all())),
                'start_date': self.start_date,
                'end_date': self.end_date,
                }

    @property
    def duration(self):
        return (self.end_date - self.start_date).days

    def total_price(self):
        price = 0
        for option in self.options.values():
            price += option['base_price'] + self.duration * option['daily_price']
        return price

    class Meta:
        verbose_name = 'Выбранное предложение'
        verbose_name_plural = 'Выбранные предложения'
