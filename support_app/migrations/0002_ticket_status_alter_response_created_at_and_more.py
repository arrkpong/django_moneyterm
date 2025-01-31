# Generated by Django 5.0.4 on 2024-06-09 01:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Open', 'เปิด'), ('Closed', 'ปิด')], default='Open', max_length=10, verbose_name='สถานะ'),
        ),
        migrations.AlterField(
            model_name='response',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='สร้างเมื่อ'),
        ),
        migrations.AlterField(
            model_name='response',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='response_images/', verbose_name='รูปภาพ'),
        ),
        migrations.AlterField(
            model_name='response',
            name='message',
            field=models.TextField(verbose_name='ข้อความ'),
        ),
        migrations.AlterField(
            model_name='response',
            name='responder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ผู้ตอบ'),
        ),
        migrations.AlterField(
            model_name='response',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='support_app.ticket', verbose_name='ตั๋ว'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='สร้างเมื่อ'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ผู้ใช้งาน'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_images/', verbose_name='รูปภาพ'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='message',
            field=models.TextField(verbose_name='ข้อความ'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='หัวข้อ'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='อัปเดตเมื่อ'),
        ),
    ]
