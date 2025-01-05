# Generated by Django 5.0.4 on 2024-05-22 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_alter_notification_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='advertisement_image',
            field=models.ImageField(blank=True, null=True, upload_to='advertisement_images/', verbose_name='Advertisement Image'),
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Advertisement Title'),
        ),
    ]
