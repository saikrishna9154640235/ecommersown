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



def Login(request):
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")
        
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                 return redirect("login")
        return render (request,"login.html")

@login_required
def Logout(request):
    logout(request)
    return redirect("login")


