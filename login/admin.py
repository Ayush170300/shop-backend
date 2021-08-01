from django.contrib import admin
from login.models import Product,Order

# Register your models here.
admin.site.register((Product))
admin.site.register((Order))