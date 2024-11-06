from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.transaction import atomic
from django.utils import timezone
from .models import Order, OrderItem, OrderService
from .forms import OrderForm, OrderItemForm, OrderServiceForm
from accounts.models import Customer
from products.models import Product, Service

@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    if request.user.role == 'sales':
        orders = orders.filter(sales_person=request.user)
    elif request.user.role == 'workshop':
        orders = orders.filter(
            items__services__assigned_to=request.user,
            status='in_progress'
        ).distinct()
    
    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)

@login_required
@atomic
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.sales_person = request.user
            order.total_amount = 0
            order.save()
            messages.success(request, 'Order created successfully.')
            return redirect('order_detail', pk=order.pk)
    else:
        initial = {}
        if customer_id := request.GET.get('customer'):
            initial['customer'] = customer_id
        form = OrderForm(initial=initial)
    
    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Create New Order'
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        if 'add_item' in request.POST:
            item_form = OrderItemForm(request.POST)
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.order = order
                product = item.product
                if product.is_glass_type:
                    item.unit_price = product.calculate_price(item.width, item.height)
                else:
                    item.unit_price = product.unit_price
                item.save()
                messages.success(request, 'Item added successfully.')
                return redirect('order_detail', pk=pk)
        elif 'add_service' in request.POST:
            service_form = OrderServiceForm(request.POST)
            if service_form.is_valid():
                service = service_form.save(commit=False)
                service.price = service.service.base_price
                if service.pattern:
                    service.price += service.pattern.price
                service.save()
                messages.success(request, 'Service added successfully.')
                return redirect('order_detail', pk=pk)
    
    item_form = OrderItemForm()
    service_form = OrderServiceForm()
    
    context = {
        'order': order,
        'item_form': item_form,
        'service_form': service_form,
    }
    return render(request, 'orders/order_detail.html', context)

@login_required
def update_order_status(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def update_payment_status(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        payment_status = request.POST.get('payment_status')
        paid_amount = request.POST.get('paid_amount')
        if payment_status in dict(Order.PAYMENT_STATUS):
            order.payment_status = payment_status
            if paid_amount:
                order.paid_amount = float(paid_amount)
            order.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def update_service_status(request, order_id, service_id):
    if request.method == 'POST':
        service = get_object_or_404(OrderService, order_item__order_id=order_id, id=service_id)
        new_status = request.POST.get('status')
        if new_status in dict(OrderService.STATUS_CHOICES):
            service.status = new_status
            if new_status == 'done':
                service.completed_at = timezone.now()
            service.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def order_receipt(request, pk):
    order = get_object_or_404(Order, pk=pk)
    html = render_to_string('orders/receipt.html', {'order': order})
    return HttpResponse(html)