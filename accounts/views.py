from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from .forms import CustomerForm
from .models import Customer
from orders.models import Order
from products.models import Product
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    # Get statistics for the dashboard
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    context = {
        'total_orders': Order.objects.filter(order_date__date=today).count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'monthly_sales': Order.objects.filter(
            order_date__date__gte=thirty_days_ago
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        'low_stock_products': Product.objects.filter(
            stock__lte=models.F('min_stock')
        ).count(),
    }
    
    if request.user.role in ['admin', 'accountant']:
        # Additional statistics for admin/accountant
        context.update({
            'unpaid_orders': Order.objects.filter(
                payment_status__in=['not_paid', 'partially_paid']
            ).count(),
            'total_revenue': Order.objects.filter(
                order_date__date__gte=thirty_days_ago
            ).aggregate(total=Sum('paid_amount'))['total'] or 0,
        })
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'accounts/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    return render(request, 'accounts/customer_form.html', {'form': form, 'title': 'Add Customer'})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = Order.objects.filter(customer=customer).order_by('-order_date')
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders.count(),
        'total_spent': orders.aggregate(total=Sum('total_amount'))['total'] or 0,
    }
    return render(request, 'accounts/customer_detail.html', context)

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'accounts/customer_form.html', {
        'form': form,
        'title': 'Edit Customer',
        'customer': customer
    })