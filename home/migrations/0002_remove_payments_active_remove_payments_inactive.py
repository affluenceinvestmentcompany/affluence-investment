# Generated by Django 5.1.5 on 2025-02-15 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='active',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='inactive',
        ),
    ]
