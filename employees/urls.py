from django.urls import path
from .views import employee_list, add_employee, update_employee, delete_employee

urlpatterns = [
    path('', employee_list),
    path('add/', add_employee),
    path('update/<int:id>/', update_employee),
    path('delete/<int:id>/', delete_employee),
]