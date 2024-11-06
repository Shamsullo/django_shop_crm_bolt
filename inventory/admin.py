from django.contrib import admin
from .models import InventoryTransaction, Supplier

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'transaction_type', 'quantity', 'unit_price', 'total_price', 'created_by', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('product__name', 'reference')
    readonly_fields = ('total_price',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'phone', 'email')