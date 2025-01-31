# Generated by Django 5.0.2 on 2024-02-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='pin',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='PIN'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='serial_number',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Serial Number'),
        ),
    ]
