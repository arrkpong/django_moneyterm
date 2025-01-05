# products_app/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CardType, CardPrice, CardDetail, Advertisement, Promotion

class CardTypeAdmin(admin.ModelAdmin):
    list_display = ["card_name", "is_popular", "display_image"]
    list_editable = ["is_popular"]
    search_fields = ["card_name"]
    list_filter = ["is_popular"]
    list_per_page = 10

    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        else:
            return "No Image"
    display_image.short_description = 'Image'

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

class CardPriceAdmin(admin.ModelAdmin):
    list_display = ["card_price", "price", "quantity"]
    search_fields = ["card_price__card_name", "price"]
    list_filter = ["card_price__card_name"]
    list_per_page = 10
    readonly_fields = ["quantity"]

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

class CardDetailAdmin(admin.ModelAdmin):
    list_display = ["card_detail", "serial_number", "pin", "get_price", "is_active", "add_date"]
    search_fields = ["card_detail__card_price__card_name", "serial_number", "card_detail__price"]
    list_filter = ["card_detail__card_price__card_name", "is_active", "card_detail__price"]
    list_per_page = 10
    readonly_fields = ["is_active"]
    #list_editable = ["is_active"]
    
    def get_price(self, obj):
        return obj.card_detail.price
    get_price.short_description = 'price'

    def card_type(self, obj):
        return obj.card_detail.card_price.card_name
    card_type.admin_order_field = 'card_detail__card_price__card_name'

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ["display_image", "description", "created_at"]
    search_fields = ["description"]
    list_per_page = 10

    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        else:
            return "No Image"
    display_image.short_description = 'Image'

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

class PromotionAdmin(admin.ModelAdmin):
    list_display = ["card_price", "discount_percentage", "start_date", "end_date"]
    search_fields = ["card_price__card_price__card_name"]
    list_filter = ["start_date", "end_date"]
    list_per_page = 10

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

admin.site.register(CardType, CardTypeAdmin)
admin.site.register(CardPrice, CardPriceAdmin)
admin.site.register(CardDetail, CardDetailAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
#admin.site.register(Promotion, PromotionAdmin)

