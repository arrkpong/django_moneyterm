from django.contrib import admin
from .models import Ticket, Response

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    readonly_fields = ('responder', 'message', 'image', 'created_at')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'subject', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'subject', 'message')
    inlines = [ResponseInline]
    readonly_fields = ('customer', 'subject', 'message', 'image', 'status', 'created_at', 'updated_at')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'responder', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ticket__subject', 'responder__username', 'message')
    readonly_fields = ('ticket', 'responder', 'message', 'image', 'created_at')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Response, ResponseAdmin)
