from django.shortcuts import render
from employees.models import Employee
from inventory.models import Product
from purchase.models import Purchase
from sales.models import Sale
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


@login_required(login_url='/login/')
def home(request):
    total_employees = Employee.objects.count()
    total_products = Product.objects.count()
    total_purchases = Purchase.objects.count()
    total_sales = Sale.objects.count()

    total_stock = 0
    products = Product.objects.all()

    for product in products:
        total_stock += product.quantity

    return render(request, 'home.html', {
        'total_employees': total_employees,
        'total_products': total_products,
        'total_purchases': total_purchases,
        'total_sales': total_sales,
        'total_stock': total_stock,
    })
    

def logout_view(request):
    logout(request)
    return redirect('/login/')