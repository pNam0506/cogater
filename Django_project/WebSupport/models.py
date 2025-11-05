from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=30)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # ← ฟิลด์เก็บรูป
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name