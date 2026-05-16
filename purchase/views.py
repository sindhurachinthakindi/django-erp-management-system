from django.shortcuts import render, redirect
from .models import Purchase, PurchaseItem
from inventory.models import Product
from django.contrib import messages


def add_purchase(request):
    if request.method == 'POST':
        supplier = request.POST.get('supplier')

        if not supplier:
            messages.error(request, "Supplier name is required")
            return redirect('/purchase/add/')

        purchase = Purchase.objects.create(
            supplier=supplier
        )

        return redirect(f'/purchase/item/{purchase.id}/')

    return render(request, 'add_purchase.html')


def add_purchase_item(request, id):
    purchase = Purchase.objects.get(id=id)
    products = Product.objects.all()
    items = PurchaseItem.objects.filter(purchase=purchase)

    total = 0
    for item in items:
        total += item.quantity

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')

        if not product_id:
            messages.error(request, "Please select a product")
            return redirect(f'/purchase/item/{id}/')

        if not quantity:
            messages.error(request, "Quantity is required")
            return redirect(f'/purchase/item/{id}/')

        try:
            quantity = int(quantity)

            if quantity <= 0:
                messages.error(request, "Quantity must be greater than 0")
                return redirect(f'/purchase/item/{id}/')

            product = Product.objects.get(id=product_id)

            existing_item = PurchaseItem.objects.filter(
                purchase=purchase,
                product=product
            ).first()

            # increase stock
            product.quantity += quantity
            product.save()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                PurchaseItem.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=quantity
                )

            messages.success(request, "Item added successfully")

        except Product.DoesNotExist:
            messages.error(request, "Product not found")

        except Exception:
            messages.error(request, "Something went wrong")

        return redirect(f'/purchase/item/{id}/')

    return render(request, 'add_purchase_item.html', {
        'purchase': purchase,
        'products': products,
        'items': items,
        'total': total
    })


def purchase_detail(request, id):
    purchase = Purchase.objects.get(id=id)
    items = PurchaseItem.objects.filter(purchase=purchase)

    return render(request, 'purchase_detail.html', {
        'purchase': purchase,
        'items': items
    })


def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-id')

    return render(request, 'purchase_list.html', {
        'purchases': purchases
    })


def delete_purchase_item(request, id):
    item = PurchaseItem.objects.get(id=id)

    product = item.product
    product.quantity -= item.quantity
    product.save()

    purchase_id = item.purchase.id
    item.delete()

    messages.success(request, "Item deleted successfully")

    return redirect(f'/purchase/item/{purchase_id}/')


def delete_purchase(request, id):
    purchase = Purchase.objects.get(id=id)
    items = PurchaseItem.objects.filter(purchase=purchase)

    for item in items:
        item.product.quantity -= item.quantity
        item.product.save()

    purchase.delete()

    messages.success(request, "Purchase deleted successfully")

    return redirect('/purchase/')