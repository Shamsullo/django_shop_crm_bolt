from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/update-status/', views.update_order_status, name='update_order_status'),
    path('<int:pk>/update-payment/', views.update_payment_status, name='update_payment_status'),
    path('<int:order_id>/services/<int:service_id>/update/', views.update_service_status, name='update_service_status'),
    path('receipt/<int:pk>/', views.order_receipt, name='order_receipt'),
]