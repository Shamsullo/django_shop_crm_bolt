from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InventoryTransaction, Supplier
from .forms import InventoryTransactionForm, SupplierForm

@login_required
def inventory_list(request):
    transactions = InventoryTransaction.objects.all().order_by('-created_at')
    return render(request, 'inventory/inventory_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = InventoryTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, 'Transaction recorded successfully.')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = InventoryTransactionForm()
    
    return render(request, 'inventory/transaction_form.html', {
        'form': form,
        'title': 'New Transaction'
    })

@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(InventoryTransaction, pk=pk)
    return render(request, 'inventory/transaction_detail.html', {'transaction': transaction})

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, 'Supplier added successfully.')
            return redirect('supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm()
    
    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Add Supplier'
    })

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'inventory/supplier_detail.html', {'supplier': supplier})

@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully.')
            return redirect('supplier_detail', pk=pk)
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Edit Supplier',
        'supplier': supplier
    })