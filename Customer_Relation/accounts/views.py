from django.shortcuts import render,redirect
from .models import  *
from .forms import  orderForm,CreateuserForm,CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
# Create your views here.

@unauthenticated_user
def registerPage(request):

    form = CreateuserForm()
    if request.method == 'POST':
        form = CreateuserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Acccount was successfully created for ' + username)
            return redirect('login')



    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username or Password incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()


    context = {'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending,'orders':orders}
    return render(request,'accounts/home.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    print("Orders:", orders)
    context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}

    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}

    return render(request, 'accounts/accounts_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()

    context = {'product':product}
    return render(request,'accounts/products.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,customer_id):
    customer = Customer.objects.get(id=customer_id)
    order = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs



    context = {'customer':customer, 'order':order,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(request,customer_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=8)
    customer = Customer.objects.get(id=customer_id)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == "POST":
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
def updateOrder(request,order_id):
    order = Order.objects.get(id=order_id)
    form = orderForm(instance=order)
    if request.method == 'POST':
        form = orderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
def deleteOrder(request,delete_id):
    delete_item = Order.objects.get(id=delete_id)
    if request.method == "POST":
        delete_item.delete()
        return redirect('/')

    context={'delete_item':delete_item}
    return render(request,'accounts/delete.html',context)