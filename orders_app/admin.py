# orders_app/admin.py
from django.contrib import admin
from .models import Order, OrderItem, Feedback

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'rating', 'comment', 'created_at')
    readonly_fields = ('order', 'user', 'rating', 'comment', 'created_at')
    list_filter = ['rating']
    list_per_page = 10

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

admin.site.register(Feedback, FeedbackAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'card', 'amount', 'price', 'serial_number', 'pin')
    readonly_fields = ('order', 'card', 'amount', 'price', 'serial_number', 'pin')
    list_per_page = 10

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

admin.site.register(OrderItem, OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'order_date', 'status')
    readonly_fields = ('id', 'user', 'total_price', 'order_date', 'status')
    inlines = [OrderItemInline]
    list_filter = ['order_date', 'status']
    date_hierarchy = 'order_date'
    list_per_page = 10

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

admin.site.register(Order, OrderAdmin)

