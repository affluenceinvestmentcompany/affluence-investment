# Generated by Django 5.1.5 on 2025-02-15 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_transaction_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.payments'),
        ),
    ]
