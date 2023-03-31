from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('cart/', get_cart, name = 'cart'),
    re_path(r'add_cart/(?P<product_id>[0-9]{1,4})/', add_to_cart, name='add_to_cart'),
    re_path(r'update_cart/(?P<product_id>[0-9]{1,4})/', update_to_cart, name='update_to_cart'),
    re_path(r'remove_from_cart/(?P<product_id>[0-9]{1,4})/', remove_from_cart, name='remove_from_cart'),
]