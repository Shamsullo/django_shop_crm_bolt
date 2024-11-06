from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    SALES = 'sales'
    WORKSHOP = 'workshop'
    ACCOUNTANT = 'accountant'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (SALES, 'Sales Manager'),
        (WORKSHOP, 'Workshop Master'),
        (ACCOUNTANT, 'Accountant'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=SALES)
    phone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name