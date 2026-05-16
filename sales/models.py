from django.db import models
from inventory.models import Product

class Sale(models.Model):
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
