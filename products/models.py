from django.db import models
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Glass/Mirror specific fields
    is_glass_type = models.BooleanField(default=False)
    thickness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_width = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    max_height = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_price(self, width=None, height=None):
        if self.is_glass_type and width and height:
            area = Decimal(width) * Decimal(height)
            return self.unit_price * area
        return self.unit_price

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Pattern(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='patterns/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name