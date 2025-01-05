# user_app/admin.py

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'phone_number', 'date_of_birth', 'enable_two_factor', 'receive_notification']
    list_filter = ['enable_two_factor', 'receive_notification']
    search_fields = ['user__username', 'bio', 'phone_number']
    readonly_fields = ['user']

    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Additional Information', {'fields': ('bio', 'profile_image', 'phone_number', 'date_of_birth', 'enable_two_factor', 'receive_notification')}),
    )

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    
'''from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'message', 'created_at', 'receive_notification']
    list_filter = ['receive_notification']
    search_fields = ['user__username', 'message']
    readonly_fields = ['created_at']

    def save_model(self, request, obj, form, change):
        # Call the save method of the Notification model which includes the email logic
        obj.save()

    def delete_model(self, request, obj):
        # Delete the advertisement_image file if it exists
        if obj.advertisement_image:
            obj.advertisement_image.delete()
        # Call the delete method of the Notification model
        obj.delete()'''

#admin.site.register(Notification, NotificationAdmin)
