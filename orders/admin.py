from django.contrib import admin
from .models import Order, OrderItem, OrderService

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 0
    fields = ('service', 'pattern', 'status', 'assigned_to', 'price')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'width', 'height', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'sales_person', 'status', 'payment_status', 'total_amount', 'order_date')
    list_filter = ('status', 'payment_status', 'order_date')
    search_fields = ('customer__name', 'sales_person__username')
    inlines = [OrderItemInline, OrderServiceInline]
    readonly_fields = ('total_amount',)