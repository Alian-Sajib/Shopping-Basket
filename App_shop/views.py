from django.shortcuts import render

# import views
from django.views.generic import ListView, DetailView

# models
from App_shop.models import Catagory, Product

#mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'App_shop/home.html'

class ProductDetail(DetailView):
    model = Product
    template_name = 'App_shop/product_detail.html'