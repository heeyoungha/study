from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_price', 'item_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = '총 금액'
    
    def item_count(self, obj):
        return obj.cartitem_set.count()
    item_count.short_description = '아이템 수'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cart__user__username', 'product__name']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = '총 금액'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    list_editable = ['status', 'payment_status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'product__name']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = '총 금액'
