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
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата отчета')),
                ('link', models.URLField(verbose_name='ссылка на контент')),
                ('start_guide', models.BooleanField(default=False, verbose_name='По гайду')),
                ('type', models.CharField(blank=True, choices=[('review', 'Отзыв'), ('content', 'Контент'), ('photo', 'Фото с мерчем')], null=True, verbose_name='Тип контента')),
                ('platform', models.CharField(blank=True, choices=[('habr', 'Хабр'), ('VC', 'VC'), ('youtube', 'Youtube'), ('telegram', 'Телеграм'), ('instagram', 'Инстаграм'), ('linkedin', 'lLinkedin'), ('other', 'Прочее')], max_length=9, null=True, verbose_name='Площадка')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий менеджера')),
                ('accepted', models.BooleanField(default=False, verbose_name='Заявка принята')),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_content', to='ambassadors.ambassador', verbose_name='Амбассадор')),
            ],
            options={
                'verbose_name': 'Контент',
                'verbose_name_plural': 'Контент',
                'ordering': ('-created_at', 'ambassador'),
            },
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Промокод должен состоять из заглавных букв и цифр', regex='[А-ЯA-Z0-9]+')], verbose_name='промокод')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_promocode', to='ambassadors.ambassador', verbose_name='Амбассадор')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.URLField(verbose_name='Ссылка на документ')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='content.content', verbose_name='Контент_id')),
            ],
            options={
                'verbose_name': 'Доп.документ',
                'verbose_name_plural': 'Доп.документы',
                'ordering': ('content',),
            },
        ),
    ]
