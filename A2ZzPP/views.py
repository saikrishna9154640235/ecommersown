from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required
def Home(request):
    products=Product.objects.all()
    cart_item=Cart_item.objects.all()
    ans=0
    for c in cart_item:
        ans+=1
    
 
    return render(request,"home.html",{"products":products,"ans":ans})
def Contact(request):
    return render(request,"contact.html")

def More_details(request,id):
    product=Product.objects.get(id=id)
    context={"product":product}
    return render(request,"moredetails.html",context)

from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, Cart_item

def cart(request, pro_id):
    user = request.user
    product = get_object_or_404(Product, id=pro_id)
    carts, created = Cart.objects.get_or_create(user=user, is_paid=False)

    # Create the cart item
    Cart_item.objects.create(cart=carts, product=product)

    return redirect("home")

from django.db.models import Sum
def cart_items(request):
    no_of_items=Cart_item.objects.all()

    suming=Cart_item.objects.aggregate(sumings=Sum("product__price"))
    s=suming
    v=s['sumings']
    return render(request,'cart.html',{"no_of_items":no_of_items,"suming":suming,"v":v})

def Remove(request,remove):
    removes=Cart_item.objects.get(id=remove).delete()
    return redirect("cart_items")
    
    
    
    
