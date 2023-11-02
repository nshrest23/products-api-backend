from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    product_img = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'product'
    
    def __str__(self):
        return self.title
