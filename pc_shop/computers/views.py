import json
import os
from typing import Any, Dict
from django.conf import settings
from django.http import Http404

from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.views import LoginView

from .utils import normalize_price

from .tasks import send_verification_email

from .details_filter import Details
from .forms import UserAuthenticationForm, UserCreationForm
from .models import Product, Category, Specification, User


class Main(ListView):
    model = Product
    template_name = 'computers/main.html'
    context_object_name = "categories"
    queryset = Category.objects.all().order_by("id")
    
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная страница'
        return context


class Search(ListView):
    model = Product
    template_name = 'computers/search.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query")
        context["title"] = f"Поиск по запросу - {self.request.GET.get('query')}"
        return context
    
    def get_queryset(self):
        request = self.request.GET.get("query")
        return Product.objects.filter( Q(name__icontains = request) | Q(category__name = request) | Q(category__plural_name = request) ).order_by("category_id")

class SearchFilter(ListView):
    model = Product
    template_name = 'computers/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Details(self.request).get_ready_data()

class DescriptionProduct(DetailView):
    model = Product
    template_name = 'computers/product.html'
    context_object_name = "post"
    slug_url_kwarg = "post_slug"


class Authorization(LoginView):
    form_class = UserAuthenticationForm
    template_name = "authentication/login.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context
    
    def get_success_url(self):
        return reverse_lazy('main')



class Registration(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('main')
    template_name = 'authentication/registration.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context
    
    #def form_valid(self, form):
    #    user = form.save()
        # login(self.request, user)
    #    return redirect('main')

def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_confirmation=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")
    user.is_confirmation = True
    user.save()

    return redirect('main')


def logout_user(request):
    logout(request)
    return redirect('main')


