# Generated by Django 5.0.4 on 2024-05-21 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0012_revenuesummary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revenuesummary',
            name='date',
        ),
        migrations.AddField(
            model_name='revenuesummary',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders_app.order', verbose_name='คำสั่งซื้อ'),
        ),
    ]
