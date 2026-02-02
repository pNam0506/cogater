from django.db import models

# Create your models here.
class sign_com(models.Model):
    username_com = models.CharField(max_length=100)
    email_com = models.CharField(max_length=100)
    image_com = models.ImageField(upload_to='product_images/', blank=True, null=True)
    password_com = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username_com

class Company(models.Model):
    
    company = models.ForeignKey(sign_com, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    store = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    operator = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=30)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # ← ฟิลด์เก็บรูป
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    