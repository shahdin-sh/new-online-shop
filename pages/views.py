from django.shortcuts import render
from django.db.models.aggregates import Count, Avg
from cart.cart import Cart
from products.models import Product, Comment, Category, Discount
from orders.models import OrderItem
from django.db.models import F, Q, Subquery, OuterRef, ForeignKey, Value, ExpressionWrapper, Count, Max, Min, Avg, Func, DecimalField, Case, When, CharField
from django.db import models



def homepage(request):
    return render(request, 'home.html')

