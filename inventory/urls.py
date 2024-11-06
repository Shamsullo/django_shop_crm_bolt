from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('transaction/create/', views.transaction_create, name='transaction_create'),
    path('transaction/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
]