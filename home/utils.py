import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except: 
        cart = {}
    print('Cart: ',cart)  
    items = []
    order = {'get_cart_items': 0,'get_cart_total': 0}
    cartItems = order['get_cart_items']

    for i in cart :
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.pro_price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'pro_name': product.pro_name,
                    'pro_price': product.pro_price,
                    'pro_img': product.pro_img
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)
        except:
            pass
    return {'cartItems' : cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']
        cartItems = cookieData['cartItems']
    return {'cartItems' : cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(email=email)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['product']['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return customer, order