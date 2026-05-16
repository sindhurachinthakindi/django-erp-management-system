from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchase_list, name='purchase_list'),
    path('add/', views.add_purchase, name='add_purchase'),
    path('item/<int:id>/', views.add_purchase_item, name='add_purchase_item'),
    path('delete-item/<int:id>/', views.delete_purchase_item, name='delete_purchase_item'),
    path('delete/<int:id>/', views.delete_purchase, name='delete_purchase'),
]
