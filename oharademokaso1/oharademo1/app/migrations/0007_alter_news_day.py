# Generated by Django 4.1.3 on 2022-12-07 01:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_news_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='day',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日付'),
        ),
    ]