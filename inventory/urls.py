from django.urls import path
from .views import product_list, add_product, update_product, delete_product

urlpatterns = [
    path('', product_list),
    path('add/', add_product),
    path('update/<int:id>/', update_product),
    path('delete/<int:id>/', delete_product),
]