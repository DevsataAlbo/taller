from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'purchase_price', 'sale_price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code')