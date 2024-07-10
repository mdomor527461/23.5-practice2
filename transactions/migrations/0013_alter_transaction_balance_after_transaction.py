# Generated by Django 5.0.6 on 2024-06-26 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_transaction_balance_after_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='balance_after_transaction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
