# Generated by Django 5.1.5 on 2025-02-20 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_investments_amount_alter_investments_roi_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investments',
            options={},
        ),
        migrations.AddField(
            model_name='investments',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investments',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='investments',
            name='plan',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='investments',
            name='roi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
    ]
