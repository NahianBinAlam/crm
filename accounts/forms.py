from django.forms import ModelForm
from .models import order 

class OrderForm(ModelForm):
	"""docstring for orderform"""
	class Meta:
		model = order
		fields = '__all__'
		