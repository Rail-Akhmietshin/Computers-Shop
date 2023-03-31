from django import template
from cart.cart import Cart
from computers.models import Product


register = template.Library()

@register.simple_tag
def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.unit_price, quantity)