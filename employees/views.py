from django.shortcuts import render, redirect
from .models import Employee

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'list.html', {'employees': employees})

def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        salary = request.POST.get('salary')
        
        Employee.objects.create(
            name=name,
            email=email,
            salary=salary
        )
        
        return redirect('/employees/')
    return render(request, 'add.html')

def update_employee(request, id):
    emp = Employee.objects.get(id=id)
    
    if request.method == 'POST':
        emp.name = request.POST.get('name')
        emp.email = request.POST.get('email')
        emp.salary = request.POST.get('salary')
        emp.save()
        
        return redirect('/employees/')
    return render(request, 'update.html', {'emp':emp})

def delete_employee(request, id):
    emp = Employee.objects.get(id=id)
    emp.delete()
    return redirect('/employees/')