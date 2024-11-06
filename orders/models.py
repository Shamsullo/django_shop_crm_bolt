from django.db import models
from accounts.models import User, Customer
from products.models import Product, Service, Pattern

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('not_paid', 'Not Paid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='not_paid')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    width = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.product.is_glass_type and self.width and self.height:
            self.total_price = self.product.calculate_price(self.width, self.height) * self.quantity
        else:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class OrderService(models.Model):
    STATUS_CHOICES = [
        ('in_queue', 'In Queue'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_queue')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.service.name} for Order #{self.order_item.order.id}"