# Generated by Django 4.1.3 on 2022-12-06 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_news_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='Siyouritu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='席番号')),
                ('kazu', models.IntegerField(default=0)),
            ],
        ),
    ]
