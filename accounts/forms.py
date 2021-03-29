from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = customer
		fields = '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
	"""docstring for orderform"""
	class Meta:
		model = order
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User 
		fields = {'email','password1','password2','username'}
		