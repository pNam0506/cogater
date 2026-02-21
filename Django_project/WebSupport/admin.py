from django.contrib import admin
from WebSupport.models import Product, Company, sign_com

# Register your models here.
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(sign_com)
