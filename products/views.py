from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Service, Pattern
from .forms import ProductForm, ServiceForm, PatternForm

@login_required
def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Edit Product',
        'product': product
    })

@login_required
def service_list(request):
    services = Service.objects.all().order_by('name')
    return render(request, 'products/service_list.html', {'services': services})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            messages.success(request, 'Service created successfully.')
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm()
    
    return render(request, 'products/service_form.html', {
        'form': form,
        'title': 'Add Service'
    })

@login_required
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'products/service_detail.html', {'service': service})

@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('service_detail', pk=pk)
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'products/service_form.html', {
        'form': form,
        'title': 'Edit Service',
        'service': service
    })