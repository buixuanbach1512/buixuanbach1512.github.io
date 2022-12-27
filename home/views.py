from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from .form import registerForm, loginForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
import json
import datetime
from .utils import cookieCart , cartData, guestOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

# def index(request):
#     return render(request, 'pages/home.html')

class listHome(View):
    def get(self, request):
        DataCat = Category.objects.all().order_by('date')
        DataPro = Product.objects.all().order_by('date')[:8]

        data = cartData(request)
        order = data['order']
        items = data['items']
        cartItems = data['cartItems']

        context = ({'Categories' : DataCat, 'Product' : DataPro, 'cartItems': cartItems})
        return render(request, 'pages/home.html', context)

def show_product(request, cat_id):
    DataCat = Category.objects.all().order_by('date')
    Cate_prod = Category.objects.get(id=cat_id)
    DataPro = Product.objects.filter(cat_id=cat_id)
    paginator = Paginator(DataPro, 9)

    pageNumber = request.GET.get('page')
    try:
        products = paginator.page(pageNumber)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = { 
        'Product' : products,
        'Categories' : DataCat,
        'cartItems' : cartItems,
        'Category' : Cate_prod,
        }
    return render(request, 'pages/products.html', context )

class register(View):
    def get(self, request):
        rF = registerForm
        context = ({'rF' : rF})
        return render(request, 'pages/register.html', context)
    def post(self, request):
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']

        user = User.objects.create_user(username, email, password)
        user.save()

        Customer.objects.create(
            user = user,
            name = user.username,
            email = user.email
        )  

        messages.success(request,"Đăng ký thành công !!!")
        return redirect('/register')
    
class loginUser(View):
    def get(self, request):
        lF = loginForm
        context = ({'lF': lF})
        return render(request, 'pages/login.html', context)
    
    def post(self, request):
        username= request.POST['username']
        password= request.POST['password']

        user = authenticate( username = username, password = password)
        if user is not None :
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,"Đăng nhập thất bại !!!")
            return redirect('/login')

class logoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('/')

def show_product_detail(request, pro_id):
    DataPro = Product.objects.get(pk=pro_id)
    DataCat = Category.objects.all().order_by('date')

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = ({'Product' : DataPro, 'Categories' : DataCat, 'cartItems': cartItems})
    return render(request, 'pages/detail.html', context)

def cart(request):
    DataCat = Category.objects.all().order_by('date')

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order , 'Categories' : DataCat, 'cartItems': cartItems}
    return render(request,'pages/cart.html', context)

def checkout(request):
    DataCat = Category.objects.all().order_by('date')

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order , 'Categories' : DataCat, 'cartItems': cartItems}
    return render(request,'pages/checkout.html', context)

def updateItem (request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action: ',action)
    print('Product: ', productID)

    customer = request.user.customer
    product = Product.objects.get(id= productID)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        phone=data['shipping']['phone'],
    )

    return JsonResponse('Payment submitted..', safe=False)

def seachProduct(request):
    DataCat = Category.objects.all().order_by('date')
    if 'q' in request.GET :
        q = request.GET['q']
        data = Product.objects.filter(pro_name__icontains = q)
    
    paginator = Paginator(data, 9)

    pageNumber = request.GET.get('page')
    try:
        products = paginator.page(pageNumber)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = {
        'data': products,
        'Categories': DataCat,
        'q' : q,
        'cartItems': cartItems
    }
    return render(request, 'pages/search.html', context)

def contact(request):
    DataCat = Category.objects.all().order_by('date')
    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    context = {'Categories': DataCat, 'cartItems': cartItems}
    return render(request, 'pages/contact.html', context)

