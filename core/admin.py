from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Color, ProductSize, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ['size', 'price', 'stock_quantity', 'is_available']

class ColorInline(admin.TabularInline):
    model = Color
    extra = 1
    fields = ['name', 'hex_code']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'gender', 'base_price', 'is_active', 'created_at']
    list_filter = ['category', 'gender', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['base_price']
    inlines = [ProductSizeInline, ColorInline]

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'product']
    list_filter = ['product']
    search_fields = ['name', 'product__name']

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price', 'stock_quantity', 'is_available']
    list_filter = ['is_available', 'size', 'product__category']
    search_fields = ['product__name', 'size']
    ordering = ['product__name', 'size']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'total_items', 'total_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session_id']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    ordering = ['-created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'size', 'color', 'quantity', 'price_per_unit', 'total_price']
    list_filter = ['cart__created_at', 'product__category']
    search_fields = ['product__name', 'cart__session_id']
    readonly_fields = ['total_price']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'customer_name', 'phone_number']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
