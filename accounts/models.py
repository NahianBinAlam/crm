from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class customer(models.Model):
	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	Phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png",null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class tag(models.Model):
	name = models.CharField(max_length=200, null=True)
	

	def __str__(self):
		return self.name


class product(models.Model):
	CATEGORY =(
		('Indoor' , 'Indoor'),
		('Out Door' , 'Out Door'),
		)

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tag = models.ManyToManyField(tag)

	def __str__(self):
		return self.name





class order(models.Model):
	STATUS = (
		('Pending' , 'Pending'),
		('Out for delivery' , 'Out for delivery'),
		)

	customer = models.ForeignKey(customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)
	