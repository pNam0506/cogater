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
    
    company_id = models.ForeignKey(sign_com, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    store = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    operator = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
# class Product(models.Model):
    
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     size = models.CharField(max_length=10)
#     color = models.CharField(max_length=30)
#     image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # ← ฟิลด์เก็บรูป
#     created_at = models.DateTimeField(auto_now_add=True)
#     date = models.DateField(auto_now_add=True)
#     time = models.TimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class Report(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    
    description = models.CharField(max_length=255)

    COLLAB_CHOICES = [
        ('Cartoon', 'Cartoon'),
        ('Anime', 'Anime'),
        ('Movie', 'Movie'),
        ('Game', 'Game'),
        ('Other', 'Other'),
    ]

    

    collab_type = models.CharField(max_length=50, choices=COLLAB_CHOICES)
    other_collab = models.CharField(max_length=100, blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    ads_image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ("sent", "Sent"),
        ("read", "Read"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ],
    default="sent"
)

 

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} - {self.collab_type}"
    
class CollabDocument(models.Model):
    
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    file = models.FileField(upload_to='collab_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} for Report {self.report.id}"
    
class Product(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='products'
    )

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Product {self.id} - Report {self.report.id}"
    
    
class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes'
    )

    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.size} - {self.price}" 
    
    