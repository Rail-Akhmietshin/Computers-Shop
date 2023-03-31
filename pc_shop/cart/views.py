from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

from .cart import Cart
from computers.models import Product

def add_to_cart(request, product_id=1):
    id = request.path.split("/")[-2]
    product = Product.objects.get(id=id)
    cart = Cart(request)
    cart.add(product, product.price, 1)
    return HttpResponse("")
    
def update_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = request.POST.get("quantity")
    cart = Cart(request)
    cart.update(product, quantity)
    return redirect('cart')

def remove_from_cart(request, product_id=1):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')

def get_cart(request, *args, **kwargs):
    return render(request, 'cart/basket.html', {'cart': Cart(request, *args, **kwargs)})