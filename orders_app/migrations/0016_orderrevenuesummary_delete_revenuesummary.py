# Generated by Django 5.0.4 on 2024-05-21 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0015_remove_revenuesummary_id_alter_revenuesummary_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderRevenueSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='วันที่เริ่มต้น')),
                ('end_date', models.DateField(verbose_name='วันที่สิ้นสุด')),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='รายรับรวม')),
            ],
            options={
                'verbose_name': 'สรุปรายรับจากการสั่งซื้อ',
                'verbose_name_plural': 'สรุปรายรับจากการสั่งซื้อ',
            },
        ),
        migrations.DeleteModel(
            name='RevenueSummary',
        ),
    ]
