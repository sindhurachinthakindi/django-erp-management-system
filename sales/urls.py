from django.urls import path
from .views import add_sale, add_sale_item, delete_sale_item, sales_list,sale_detail, delete_sale

urlpatterns = [
    path('', sales_list, name='sales_list'),
    path('add/', add_sale, name='add_sale'),
    path('view/<int:id>/', sale_detail, name='sale_detail'),
    path('item/<int:id>/', add_sale_item, name='add_sale_item'),
    path('delete/<int:id>/', delete_sale, name='delete_sale'),
]