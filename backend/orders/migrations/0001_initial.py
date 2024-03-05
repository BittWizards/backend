# Generated by Django 4.2.9 on 2024-03-05 05:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ambassadors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Название продукции')),
                ('cost', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 'Стоимость не может быть отрицательной')], verbose_name='Стоимость продукции')),
                ('size', models.CharField(blank=True, choices=[('XS', 'Xs'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'Xl'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45')], null=True, verbose_name='Размер для одежды')),
            ],
            options={
                'verbose_name': 'Мерч',
                'verbose_name_plural': 'Мерч',
                'ordering': ('name', 'size'),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=100, verbose_name='Отчество')),
                ('phone', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('street_home', models.CharField(max_length=200, verbose_name='Улица')),
                ('status', models.CharField(choices=[('created', 'Создано'), ('delivered', 'Доставлено'), ('shipped', 'Отправлено')], default='created', verbose_name='Статус заявки')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания заявки')),
                ('delivered_date', models.DateField(blank=True, null=True, verbose_name='Дата получения заказа')),
                ('post_index', models.IntegerField(blank=True, null=True, verbose_name='Индекс')),
                ('track_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Трек-номер')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заявке')),
                ('total_cost', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0, 'Стоимость не может быть отрицательной')], verbose_name='Полная стоимость продукции в заявке')),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ambassadors.ambassador', verbose_name='Амбассадор в заказе')),
                ('merch', models.ManyToManyField(related_name='order', to='orders.merch', verbose_name='Мерч в заявке')),
            ],
            options={
                'verbose_name': 'Заявка на отправку мерча',
                'verbose_name_plural': 'Заявка на отправку мерча',
                'ordering': ('id',),
            },
        ),
    ]
