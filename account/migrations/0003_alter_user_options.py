# Generated by Django 5.1.5 on 2025-02-15 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_resetpassword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-is_superuser', '-is_admin', '-is_staff', '-is_verified', '-date_joined']},
        ),
    ]
