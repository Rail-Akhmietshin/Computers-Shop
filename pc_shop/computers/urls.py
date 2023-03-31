from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('', Main.as_view(), name = 'main'),
    path('login/', Authorization.as_view(), name = 'login'),
    path('registration/', Registration.as_view(), name = "registration"),
    path('search/', Search.as_view(), name='search'),
    path('filters/', SearchFilter.as_view(), name='search_filter'),
    path('product/<slug:post_slug>', DescriptionProduct.as_view(), name = "product"),   
    path('logout/', logout_user, name='logout'),
    re_path(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
    path('', include('cart.urls'))
]

