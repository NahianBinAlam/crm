from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only





@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = order.objects.all()
	customers = customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status='Out for delivery').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders' :orders, 'customers' :customers, 'total_orders' :total_orders, 'delivered' :delivered , 'pending' :pending  }
	return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def products(request):
	products = product.objects.all()
	return render(request, 'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_test):
	customers = customer.objects.get(id=pk_test)
	orders = customers.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer' : customers , 'orders' : orders, 'order_count' : order_count, 'myFilter' : myFilter}
	return render(request, 'accounts/customers.html', context)
# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	orders = order.objects.get(id=pk)
	if request.method == "POST":
		orders.delete()
		return redirect('/')

	context = {'item':orders}
	return render(request, 'accounts/delete.html', context)