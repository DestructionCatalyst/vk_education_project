# Generated by Django 3.2.9 on 2021-11-11 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurance_companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('insurance_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('daily_price', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
            options={
                'verbose_name': 'Опция',
                'verbose_name_plural': 'Опции',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='PolicyHolders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('document_number', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('birth_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Застрахованный',
                'verbose_name_plural': 'Застрахованные',
                'ordering': ['-last_name'],
            },
        ),
        migrations.CreateModel(
            name='Zones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Таможенная зона',
                'verbose_name_plural': 'Таможенные зоны',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='InsuranceOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_age', models.IntegerField()),
                ('max_age', models.IntegerField()),
                ('franchise', models.DecimalField(decimal_places=2, max_digits=12)),
                ('available_options', models.ManyToManyField(to='insurance_orders.InsuranceOptions')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_companies.insurancecompanies')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_orders.zones')),
            ],
            options={
                'verbose_name': 'Страховое предложение',
                'verbose_name_plural': 'Страховые предложения',
            },
        ),
        migrations.CreateModel(
            name='InsuranceDeals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_orders.policyholders')),
                ('options', models.ManyToManyField(to='insurance_orders.InsuranceOptions')),
            ],
            options={
                'verbose_name': 'Выбранное предложение',
                'verbose_name_plural': 'Выбранные предложения',
            },
        ),
    ]
