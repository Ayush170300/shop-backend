from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
# class User(models.Model):
# 	username=models.CharField(max_length=20)
# 	password=models.CharField(max_length=20,null=False)
# 	email=models.CharField(max_length=20,null=False)

class Product(models.Model):
	product_id=models.CharField(max_length=10,null=False,unique=True)
	title=models.CharField(max_length=60,null=False)
	description=models.TextField(max_length=255,null=True)
	price=models.IntegerField(null=False)
	image_url=models.CharField(max_length=100,null=True)


class Order(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	qty=models.IntegerField(default=1)
	created_on=models.DateTimeField(default=now,blank=True)

