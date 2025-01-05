# payments/admin.py
from django.contrib import admin
from .models import OrderStatus

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['order__id', 'status']
    readonly_fields = ['order', 'status', 'timestamp']

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff