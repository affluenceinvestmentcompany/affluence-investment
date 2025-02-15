# Generated by Django 5.1.5 on 2025-02-13 22:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Investments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=100)),
                ('roi', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('date', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=255)),
                ('profit', models.CharField(max_length=100)),
                ('bonus', models.CharField(max_length=100)),
                ('min_amount', models.CharField(max_length=100)),
                ('min_days', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.CharField(max_length=255)),
                ('withdraw', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('date', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ContactUs',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='user',
        ),
        migrations.DeleteModel(
            name='ManageCard',
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
    ]
