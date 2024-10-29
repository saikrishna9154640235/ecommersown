"""
URL configuration for ecommersapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from A2ZzPP.views import *
from accounts.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",Home,name="home"),
    path("register",Register,name="register"),
    path("login",Login,name="login"),
    path("contact",Contact,name="contact"),
    path("moredetails/<id>",More_details,name="moredetails"),
    path("cart/<pro_id>",cart,name="cart"),
  
    path("remove/<remove>",Remove,name="remove"),
    path("cart_items",cart_items,name="cart_items"),


    path("logout",Logout,name="logout"),
    
    

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
