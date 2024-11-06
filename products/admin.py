from django.contrib import admin
from .models import Category, Product, Service, Pattern

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit_price', 'stock', 'is_active')
    list_filter = ('category', 'is_active', 'is_glass_type')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'description', 'unit_price', 'stock', 'min_stock', 'is_active')
        }),
        ('Glass/Mirror Properties', {
            'fields': ('is_glass_type', 'thickness', 'max_width', 'max_height'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')