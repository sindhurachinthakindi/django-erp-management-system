from django.shortcuts import render, redirect
from .models import Sale, SaleItem
from inventory.models import Product
from django.contrib import messages


def add_sale(request):
    if request.method == 'POST':
        sale = Sale.objects.create()   

        return redirect(f'/sales/item/{sale.id}/')  

    return render(request, 'add_sale.html')


def add_sale_item(request, id):
    sale = Sale.objects.get(id=id)
    products = Product.objects.all()


    items = SaleItem.objects.filter(sale=sale)
    
    total= 0
    for item in items:
        total+=item.product.price * item.quantity

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')

        if not product_id:
            messages.error(request, "Please select a product")
            return redirect(f'/sales/item/{id}/')

        if not quantity:
            messages.error(request, "Quantity is required")
            return redirect(f'/sales/item/{id}/')

        try:
            quantity = int(quantity)

            if quantity <= 0:
                messages.error(request, "Quantity must be greater than 0")
                return redirect(f'/sales/item/{id}/')

            product = Product.objects.get(id=product_id)

            existing_item = SaleItem.objects.filter(
                sale=sale,
                product=product
            ).first()

            if product.quantity < quantity:
                raise ValueError("Not enough stock available")

            product.quantity -= quantity
            product.save()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity
                )

            messages.success(request, "Item sold successfully")

        except Product.DoesNotExist:
            messages.error(request, "Product not found")

        except ValueError as e:
            messages.error(request, str(e))

        except Exception:
            messages.error(request, "Something went wrong")

        return redirect(f'/sales/item/{id}/')
    return render(request, 'add_sale_item.html', {
        'sale': sale,
        'products': products,
        'items': items,
        'total': total
    })

def delete_sale_item(request, id):
    item = SaleItem.objects.get(id=id)

    product = item.product
    product.quantity += item.quantity
    product.save()

    sale_id = item.sale.id
    item.delete()

    messages.success(request, "Item deleted successfully")

    return redirect(f'/sales/item/{sale_id}/')

def sales_list(request):
    sales = Sale.objects.all().order_by('-id')

    return render(request, 'sales_list.html', {
        'sales': sales
    })
    
def sale_detail(request, id):
    sale = Sale.objects.get(id=id)
    items = SaleItem.objects.filter(sale=sale)

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    return render(request, 'sale_detail.html', {
        'sale': sale,
        'items': items,
        'total': total
    })
    
def delete_sale(request, id):
    sale = Sale.objects.get(id=id)

    items = SaleItem.objects.filter(sale=sale)

    for item in items:
        item.product.quantity += item.quantity
        item.product.save()

    sale.delete()

    messages.success(request, "Sale deleted successfully")
    return redirect('/sales/')