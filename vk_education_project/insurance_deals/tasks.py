from celery.schedules import crontab
from django.core.mail import send_mail
from django.conf import settings
from application.celery import app
from smtplib import SMTPException
from .models import InsuranceDeals
from datetime import datetime


@app.task(autoretry_for=(SMTPException, ), max_retries=3)
def send_created_deal_mail(subject, message):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.ADMIN_EMAILS, fail_silently=False)


@app.task(autoretry_for=(Exception,))
def delete_expired_deals():
    InsuranceDeals.objects.filter(end_date__lt=datetime.now()).delete()


app.conf.beat_schedule.update(
    {
        'moderate-news-delete_expired_deals': {
            'task': 'insurance_deals.tasks.delete_expired_deals',
            'schedule': crontab(minute='*', hour='*', day_of_month='*', month_of_year='*', day_of_week='*')
        }
    }
)