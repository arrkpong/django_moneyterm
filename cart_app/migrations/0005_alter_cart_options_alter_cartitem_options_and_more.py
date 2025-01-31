# Generated by Django 5.0.4 on 2024-06-21 18:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0004_remove_cartitem_pin_remove_cartitem_serial_number'),
        ('product_app', '0005_alter_advertisement_options_alter_carddetail_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Cart', 'verbose_name_plural': 'Cart'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'CartItem', 'verbose_name_plural': 'CartItem'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='User associated with the cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='amount',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.cardprice', verbose_name='Related card'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart_app.cart', verbose_name='Related cart'),
        ),
    ]
