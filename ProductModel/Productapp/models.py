from django.db import models

# Create your models here.

class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    retailer_name = models.CharField(max_length=100, default= True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Product_Table"
