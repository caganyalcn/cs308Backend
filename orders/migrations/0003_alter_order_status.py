# Generated by Django 5.2.1 on 2025-05-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('in-transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ('refundwaiting', 'RefundWaiting'), ('refunded', 'Refunded')], default='processing', max_length=20),
        ),
    ]
