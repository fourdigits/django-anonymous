from django.db import models


class Order(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class Item(models.Model):
    order = models.ForeignKey(Order, models.CASCADE, related_name="items")
    description = models.TextField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
