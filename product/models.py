from django.db import models

class Product(models.Model):
    name = models.CharField(max_length= 300, blank= False)
    amount = models.PositiveIntegerField()

    class Meta:
        db_table = 'product_custom_title'