from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'all_orders' : orders,
        'all_customers': customers,
        'total_customers' :total_customers,
        'total_orders' : total_orders,
        'delivered' : delivered,
        'pending' : orders_pending
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')   
def product(request):
    all_products = Product.objects.all()
    context = {
        'products' : all_products
    }
    return render(request, 'products.html', context)


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    num_orders = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    order = myFilter.qs
    context = {
        'customer': customer,
        'orders' : orders,
        'num_orders' : num_orders,
        'myFilter' :myFilter,
    }
    return render(request, 'customer.html', context)



@login_required(login_url='login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=1)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        print('Creating New Order: ', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'formset': formset,
        'customer': customer
    }
    return render(request, "order_form.html", context)

@login_required(login_url='login')
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        print('Updating Order: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, "order_form.html", context )

@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item' : order
    }
    return render(request, "delete.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account created " + user)
                return redirect('login')
        context = {'form': form }
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')