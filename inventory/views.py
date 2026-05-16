from django.shortcuts import render, redirect
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products':products}) 

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )

        return redirect('/inventory/')

    return render(request, 'add_product.html')

def update_product(request, id):
    product = Product.objects.get(id=id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.save()
        
        return redirect('/inventory/')
    return render(request, 'update_product.html', {'product':product})

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('/inventory/')