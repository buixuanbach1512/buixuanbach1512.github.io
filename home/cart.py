from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Products, Cart

def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Products.objects.get(pk=prod_id)
            if product_check:
                if Cart.objects.filter(user = request.user.id, product_id = prod_id):
                    return JsonResponse({'status': 'Đã có sản phẩm trong giỏ hàng !!'})
                else: 
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty :
                        Cart.objects.create(user=request.user, product_id = prod_id, product_quantiy = prod_qty)
                        return JsonResponse({'status': 'Đã thêm sản phẩm thành công !!'})
                    else:
                        return JsonResponse({'status': 'ERROR!!'})
            else:
                return JsonResponse({'status': 'Không tìn thấy sản phẩm!!'})
        else:
            return JsonResponse({'status': 'Đăng nhập để tiếp tục'})
    return redirect('/')