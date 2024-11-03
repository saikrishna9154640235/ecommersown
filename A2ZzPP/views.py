from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings
import razorpay
# Create your views here.
@login_required(login_url='/login')
def Home(request):
    products=Product.objects.all()

    if request.GET.get('search'):
        search=request.GET.get('search')
        products=Product.objects.filter(name__icontains=search)
 
    return render(request,"home.html",{"products":products,})
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
    # Fetch the user's unpaid cart
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()

    # Check if the cart exists and is not empty
    if cart is None or cart.cart_items.count() == 0:
        return render(request, 'cart.html', {"cart": None, "vamo": 0, "total_cost": 0})

    # Count the number of items in the cart
    vamo = cart.cart_items.count()
    print(vamo)

    # Calculate total cost
    total_cost = cart.cart_items.aggregate(total_cost=Sum("product__price"))

    return render(request, 'cart.html', {"cart": cart, "vamo": vamo, "total_cost": total_cost})


def Remove(request,remove):
    removes=Cart_item.objects.get(id=remove).delete()
    return redirect("cart_items")
    
  
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.db.models import Sum
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.db.models import Sum

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required(login_url='/login')
def create_order(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(is_paid=False, user=request.user).first()
        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=404)

        total_cost = cart.cart_items.aggregate(total_cost=Sum("product__price"))['total_cost']
        if total_cost is None:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        amount = int(total_cost * 100)  # Convert to paise
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        }
        order = client.order.create(data=order_data)
        return JsonResponse({'id': order['id'], 'amount': order['amount']})
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required(login_url='/login')
def confirm_order(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        
        # Debug: Print user and payment ID
        print(f"User: {request.user}, Payment ID: {payment_id}")
        
        cart = Cart.objects.filter(is_paid=False, user=request.user).first()

        # Debug: Check if cart is found
        if cart is None:
            print("No unpaid cart found for the user.")
            return JsonResponse({'error': 'Cart not found'}, status=404)

        # Mark the cart as paid
        cart.is_paid = True
        cart.save()

        # Optional: Remove cart items if needed
        # cart.cart_items.all().delete() # Uncomment if you want to delete items

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def ispaid(request):
    user = request.user
    name=user.username
    paid_carts = Cart.objects.filter(is_paid=True, user=user)

    return render(request, "orders.html", {
        "paid_carts": paid_carts,"name":name})
