#user_app\models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    bio = models.TextField(blank=True, verbose_name='Bio')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='Profile Image')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Phone Number')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    enable_two_factor = models.BooleanField(default=False, verbose_name='Enable Two-factor Authentication')
    receive_notification = models.BooleanField(default=True, verbose_name='Receive Notifications')

    def __str__(self):
        return f'Profile of {self.user.username}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


'''class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Advertisement Title', null=True, blank=True)
    message = models.TextField(verbose_name='Message')
    advertisement_image = models.ImageField(upload_to='advertisement_images/', blank=True, null=True, verbose_name='Advertisement Image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    receive_notification = models.BooleanField(default=True, verbose_name='Receive Notification')

    def __str__(self):
        return f'Notification for {self.user.username}' if self.user else 'Notification without user'

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if created and instance.receive_notification:
        if instance.advertisement_image:  # Check if advertisement image is not None
            # สร้าง URL สำหรับรูปภาพ
            advertisement_image_url = instance.advertisement_image.url
        else:
            advertisement_image_url = None

        # รับรายชื่อผู้ใช้ที่ต้องการรับการแจ้งเตือน
        users = User.objects.filter(notification__receive_notification=True).distinct()

        # สร้างอีเมลล์สำหรับแต่ละผู้ใช้ที่ต้องการรับการแจ้งเตือน และส่งทีละรายการ
        for user in users:
            # Render the HTML template
            html_message = render_to_string('email/notification_email.html', {'title': instance.title, 'message': instance.message, 'advertisement_image': advertisement_image_url})
            subject = 'Notification'
            from_email = settings.EMAIL_HOST_USER  # Use EMAIL_HOST_USER from settings
            to_email = [user.email]  # User email

            # Create the email
            email = EmailMultiAlternatives(subject, instance.message, from_email, to_email)
            email.attach_alternative(html_message, "text/html")
            
            # Send the email
            email.send(fail_silently=False)'''



