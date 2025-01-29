from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User_info
from django.contrib.auth import authenticate,login


# Create your views here.

def index(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")

        if User_info.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")
        else:
            user=User_info(name=name,email=email,phone_number=phone)
            user.save()

        print(name,email,phone)
    return render(request,"index.html")



def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return render(request,"dashboard.html")
        else:
            return HttpResponse("Invalid credentials")

    return render(request,"login.html")