from django.db import models

from insurance_orders.models import InsuranceOptions
from insurance_orders.models import InsuranceOrders
from users.models import InsuranceUsers


# Create your models here.
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