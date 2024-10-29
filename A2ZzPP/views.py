from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required(login_url='/login')
def Home(request):
    products=Product.objects.all()
    cart=Cart.objects.filter(is_paid=False,user=request.user).first()
    vamo=cart.cart_items.count()
    print(vamo)

    if request.GET.get('search'):
        search=request.GET.get('search')
        products=Product.objects.filter(name__icontains=search)
 
    return render(request,"home.html",{"products":products,"vamo":vamo})
def Contact(request):
    return render(request,"contact.html")

def More_details(request,id):
    product=Product.objects.get(id=id)
    context={"product":product}
    return render(request,"moredetails.html",context)

from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, Cart_item
@login_required(login_url='/login')

def cart(request, pro_id):
    user = request.user
    product = get_object_or_404(Product, id=pro_id)
    carts, created = Cart.objects.get_or_create(user=user, is_paid=False)

    # Create the cart item
    Cart_item.objects.create(cart=carts, product=product)

    return redirect("home")

from django.db.models import Sum
@login_required(login_url='/login')

def cart_items(request):
    cart=Cart.objects.filter(is_paid=False,user=request.user).first()
    vamo=cart.cart_items.count()
    print(vamo)
    return render(request,'cart.html',{"cart":cart,"vamo":vamo})

def Remove(request,remove):
    removes=Cart_item.objects.get(id=remove).delete()
    return redirect("cart_items")
    
    

    
