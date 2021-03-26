from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
	orders = order.objects.all()
	customers = customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status='Out for delivery').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders' :orders, 'customers' :customers, 'total_orders' :total_orders, 'delivered' :delivered , 'pending' :pending  }
	return render(request, 'accounts/dashboard.html',context)

def products(request):
	products = product.objects.all()
	return render(request, 'accounts/products.html',{'products':products})

def customers(request, pk_test):
	customers = customer.objects.get(id=pk_test)
	orders = customers.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer' : customers , 'orders' : orders, 'order_count' : order_count, 'myFilter' : myFilter}
	return render(request, 'accounts/customers.html', context)
# Create your views here.

def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(customer, order, fields=('product','status'), extra=5 )
	customers = customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=order.objects.none(),instance=customers)
	#form = OrderForm(initial={'customer':customers})
	if request.method =='POST':
		#print('printing POST: ', request.POST)
		formset = OrderFormSet( request.POST , instance=customers)
		#form = OrderForm(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset' : formset}
	return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
	orders = order.objects.get(id=pk)
	form = OrderForm(instance=orders)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=orders)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form' : form}
	return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
	orders = order.objects.get(id=pk)
	if request.method == "POST":
		orders.delete()
		return redirect('/')

	context = {'item':orders}
	return render(request, 'accounts/delete.html', context)