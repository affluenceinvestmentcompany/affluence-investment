# Generated by Django 5.1.5 on 2025-02-14 20:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_payments_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investments',
            name='status',
        ),
        migrations.RemoveField(
            model_name='withdrawal',
            name='status',
        ),
        migrations.AddField(
            model_name='investments',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investments',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investments',
            name='pending',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='processing',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=100)),
                ('pending', models.BooleanField(default=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('date', models.TimeField(auto_now_add=True)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.payments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
