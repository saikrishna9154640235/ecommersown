from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def Register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if password1 !=password2:
            return redirect("register")
        if User.objects.filter(username=username).exists():
            return redirect("register")
        if User.objects.filter(email=email).exists():
            return redirect("register")
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password1
            
        )
          
    return  render(request, "register.html")




from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def Login(request):
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")
            #email=request.POST.get("email")
        
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                subject = 'Welcome Back!'
                message = ' you have successfully logged in.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]  # Use the email from the form
                
               
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Profile details updated.")

                return redirect("/")
            
            
            messages.warning(request, "Enter correct login user ans password")
            return redirect("login")

        return render (request,"login.html")

@login_required
def Logout(request):
    logout(request)
    return redirect("login")


